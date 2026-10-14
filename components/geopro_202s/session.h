#pragma once

#include "frame.h"
#include "poll_scheduler.h"
#include "value_decoder.h"

#include <array>
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace esphome {
namespace geopro_202s {

// The Session drops a partial Frame once no bytes have arrived for longer than this, so a
// false start (line noise, or the tail of a Reply caught at boot) can't hold back the
// Replies after it. It resets after a silence, instead of when it sends or gives up a Read
// request, because a Frame's bytes arrive about 2 ms apart at 4800 baud. A silence alone
// then shows that the held bytes will never complete a Frame, and the reset needs nothing
// from the Poll scheduler.
// 100 ms is the old hub's MESSAGE_TIMEOUT (98d6fe2^). A Frame's bytes go this long without
// a feed only when the loop stalls. The longest stall in the Node's 2026-10-09 logs, 96 ms
// in ESPHome's "took a long time" warning, was the hub publishing a Bank's Values with
// DEBUG logging, after the Reply had ended and before the next Read request went out.
// The silence before a Reply is REQUEST_GAP_MS, the 13 ms Read request and the Controller's
// latency (only the latency if the Node hears its own echo), so it can be shorter than
// 100 ms. A false start shortly before a Reply then swallows it, and the retry,
// REPLY_TIMEOUT_MS later, gets through.
static const uint32_t SILENCE_GAP_MS = 100;

// An Address is stale once this many cycles of its Poll group in a row have given up on it,
// with no Reply for it in between. A give-up is one missed cycle: the Poll scheduler drops a
// given-up Address until its next cycle, so each cycle gives up an Address at most once.
// One missed cycle isn't enough. A False start at boot can swallow a Reply and its retry, and
// tests/trace_test.cpp shows one Address missing its cycle that way; marking it stale would
// put an unknown state into Home Assistant's history, which the overnight flash check fails
// on. Two in a row means four unanswered Read requests across two cycles. A silent cycle
// takes longer than its interval when the group has many Addresses, since each give-up costs
// two REPLY_TIMEOUT_MS and a REQUEST_GAP_MS: the Node's 14 value Addresses take about 15 s.
// So at the default intervals the trace replay in tests/trace_test.cpp has a Value go unknown
// 25 to 45 s after its last Reply and a Bank setting about 140 s after, which is soon enough
// that an automation acting on a Status bit doesn't run on a frozen value for long.
static const uint8_t STALE_AFTER_MISSED_CYCLES = 2;

// Identifies one registered value. Ids count up from 0 in the order add_value() is called,
// so the hub can keep its entities in a vector indexed by id.
using EntryId = size_t;

// What a Session call produced: feed() fills `values` and `answered` from the bytes, and
// next_request() fills `missed` and `stale` from the timeouts it notices.
struct SessionOutput {
  // The Values to publish, each with the entry it belongs to.
  std::vector<DecodedValue> values;
  // The Address of each Reply received, in order, whether or not it decoded.
  std::vector<uint16_t> answered;
  // The Address of each Read request given up, in order.
  std::vector<uint16_t> missed;
  // The entries whose Address just became stale (STALE_AFTER_MISSED_CYCLES), each once. A
  // Reply for the Address, decoded or not, ends its run of misses, and the entry's next
  // decoded Value restores it.
  std::vector<EntryId> stale;
};

// The bus errors a Session has counted since it was made.
struct Counters {
  // Frames whose Checksum didn't match.
  uint32_t checksum_failures{0};
  // Received bytes that ended up in no Frame: those of a Frame whose Checksum failed, bytes
  // before a start byte, a start byte whose Length byte is out of range, and a partial Frame
  // dropped after a silence.
  uint32_t discarded_bytes{0};
  // Read requests sent again after their Reply timed out.
  uint32_t retries{0};
  // Read requests dropped until their Address's next cycle after the last retry timed out.
  uint32_t give_ups{0};
  // Replies that decoded no Values. Such a Reply still answers its Read request.
  uint32_t undecoded_replies{0};

  // Every timeout leads to a retry or a give-up.
  uint32_t timeouts() const { return this->retries + this->give_ups; }

  // The counts added since `earlier`, an older reading of the same Session. The subtraction
  // is modulo 2^32, so a count that wrapped in between still comes out right.
  Counters since(const Counters &earlier) const;

  // Whether any count is non-zero.
  bool any() const;

  // Every count with its label, for the hub's log line.
  std::string describe() const;
};

// One count in Counters and the label the log line gives it.
struct CounterField {
  uint32_t Counters::*count;
  const char *label;
};

// Every count in Counters, in the order the log line lists them. since(), any() and
// describe() loop over this, so adding a count takes a member and a row here. Timeouts have
// no row: each one is a retry or a give-up.
static const CounterField COUNTER_FIELDS[] = {
    {&Counters::checksum_failures, "checksum failures"},
    {&Counters::discarded_bytes, "discarded bytes"},
    {&Counters::retries, "retries"},
    {&Counters::give_ups, "give-ups"},
    {&Counters::undecoded_replies, "replies that decoded nothing"},
};

static_assert(sizeof(Counters) == sizeof(COUNTER_FIELDS) / sizeof(COUNTER_FIELDS[0]) * sizeof(uint32_t),
              "every count in Counters needs a row in COUNTER_FIELDS");

// The loop's decisions with no I/O: received bytes and the time go in, Read requests and
// decoded Values come out. It owns what counts as a Reply, when a request is done and
// which entry gets each Value. The hub moves bytes and Values between it and ESPHome.
// Like PollScheduler it has no clock: the caller passes millis() on every call.
class Session {
 public:
  void set_value_interval(uint32_t interval_ms) { this->scheduler_.set_value_interval(interval_ms); }
  void set_bank_interval(uint32_t interval_ms) { this->scheduler_.set_bank_interval(interval_ms); }
  uint32_t bank_interval() const { return this->scheduler_.bank_interval(); }

  // Registers a value and returns its id. The scheduler reads each Address once,
  // however many values share it.
  EntryId add_value(PollGroup group, const Registration &registration);

  const std::vector<Registration> &registrations() const { return this->registrations_; }

  SessionOutput feed(const uint8_t *bytes, size_t len, uint32_t now);

  // Returns true and sets `request` when a Read request should be sent now. A give-up is
  // noticed here, with no bytes arriving, so this is where it goes into `output`: the hub
  // publishes `output` after this call as it does after feed().
  bool next_request(uint32_t now, std::array<uint8_t, 6> &request, SessionOutput &output);

  // The counts since the Session was made. They only grow (until a count wraps at 2^32), and
  // reading them changes nothing, so a caller that wants the counts for a span keeps the
  // previous result and takes Counters::since() of it.
  Counters counters() const;

 protected:
  // How many cycles in a row have given up on an Address since its last Reply.
  struct Misses {
    uint16_t address;
    uint8_t count;
  };

  // The miss count of a registered Address, or nullptr for any other.
  Misses *find_misses_(uint16_t address);
  void on_give_up_(uint16_t address, SessionOutput &output);

  FrameDecoder decoder_;
  PollScheduler scheduler_;
  std::vector<Registration> registrations_;
  // One per registered Address, in the order the Addresses were first registered.
  std::vector<Misses> misses_;
  // The counts the Session keeps itself. The Frame codec keeps the rest.
  Counters counters_;
  // The `now` of the last bytes passed to feed().
  uint32_t last_bytes_at_{0};
};

// Decides when the hub logs a line of bus errors: at most once per interval, and only when a
// count is non-zero. The hub picks the interval and passes it on every call. Like the Session
// it has no clock; time 0 counts as the first check and the first line.
class BusErrorReport {
 public:
  // Once `interval_ms` has passed since the last check, checks `counters`, a Session's latest
  // counts. When any count has grown since the last check, returns true and sets `errors` to
  // the growth and `span_ms` to the time since the last line. Returns false otherwise.
  // Checks that find nothing only add zeros, so `errors` also holds the counts since the last
  // line.
  bool take(uint32_t now, uint32_t interval_ms, const Counters &counters, Counters &errors, uint32_t &span_ms);

 protected:
  uint32_t checked_at_{0};
  uint32_t logged_at_{0};
  Counters checked_;
};

}  // namespace geopro_202s
}  // namespace esphome
