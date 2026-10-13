#pragma once

#include "frame.h"
#include "poll_scheduler.h"
#include "value_decoder.h"

#include <array>
#include <cstddef>
#include <cstdint>
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

// Identifies one registered value. Ids count up from 0 in the order add_value() is called,
// so the hub can keep its entities in a vector indexed by id.
using EntryId = size_t;

// What the bytes passed to Session::feed() produced.
struct SessionOutput {
  // The Values to publish, each with the entry it belongs to.
  std::vector<DecodedValue> values;
  // The Address of each Reply received, in order, whether or not it decoded.
  std::vector<uint16_t> answered;
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
};

// The loop's decisions with no I/O: received bytes and the time go in, Read requests and
// decoded Values come out. It owns what counts as a Reply, when a request is done and
// which entry gets each Value. The hub moves bytes and Values between it and ESPHome.
// Like PollScheduler it has no clock: the caller passes millis() on every call.
class Session {
 public:
  void set_value_interval(uint32_t interval_ms) { this->scheduler_.set_value_interval(interval_ms); }
  void set_bank_interval(uint32_t interval_ms) { this->scheduler_.set_bank_interval(interval_ms); }

  // Registers a value and returns its id. The scheduler reads each Address once,
  // however many values share it.
  EntryId add_value(PollGroup group, const Registration &registration);

  const std::vector<Registration> &registrations() const { return this->registrations_; }

  SessionOutput feed(const uint8_t *bytes, size_t len, uint32_t now);

  // Returns true and sets `request` when a Read request should be sent now.
  bool next_request(uint32_t now, std::array<uint8_t, 6> &request);

  // The counts since the Session was made. They only grow (until a count wraps at 2^32), and
  // reading them changes nothing, so a caller that wants the counts for a span keeps the
  // previous result and takes Counters::since() of it.
  Counters counters() const;

 protected:
  FrameDecoder decoder_;
  PollScheduler scheduler_;
  std::vector<Registration> registrations_;
  // The counts the Session keeps itself. The Frame codec keeps the rest.
  Counters counters_;
  // The `now` of the last bytes passed to feed().
  uint32_t last_bytes_at_{0};
};

// Decides when the hub reports bus errors: at most once per interval, with the counts since
// the last time it checked, and only when one of them is non-zero. The hub picks the
// interval. Like the Session it has no clock; intervals start at time 0.
class BusErrorReport {
 public:
  void set_interval(uint32_t interval_ms) { this->interval_ms_ = interval_ms; }
  uint32_t interval_ms() const { return this->interval_ms_; }

  // Once an interval has passed since the last check, checks `counters`, a Session's latest
  // counts: returns true and sets `errors` to the counts since the last check when any is
  // non-zero. Returns false otherwise.
  bool take(uint32_t now, const Counters &counters, Counters &errors);

 protected:
  uint32_t interval_ms_{DEFAULT_BANK_INTERVAL_MS};
  uint32_t checked_at_{0};
  Counters checked_;
};

}  // namespace geopro_202s
}  // namespace esphome
