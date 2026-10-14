#include "doctest.h"

#include "frame.h"
#include "poll_scheduler.h"
#include "register_map.h"
#include "session.h"

#include <array>
#include <map>
#include <string>
#include <vector>

using esphome::geopro_202s::BusErrorReport;
using esphome::geopro_202s::COUNTER_FIELDS;
using esphome::geopro_202s::CounterField;
using esphome::geopro_202s::Counters;
using esphome::geopro_202s::DEFAULT_BANK_INTERVAL_MS;
using esphome::geopro_202s::EntryId;
using esphome::geopro_202s::frame_checksum;
using esphome::geopro_202s::PollGroup;
using esphome::geopro_202s::REPLY_TIMEOUT_MS;
using esphome::geopro_202s::REQUEST_GAP_MS;
using esphome::geopro_202s::Session;
using esphome::geopro_202s::SessionOutput;
using esphome::geopro_202s::SILENCE_GAP_MS;

namespace {

const uint16_t STATUS_WORD = 0x2D;

// A checksummed Frame with the given Command byte, Address and data.
std::vector<uint8_t> frame(uint8_t command, uint16_t address, const std::vector<uint8_t> &data) {
  std::vector<uint8_t> bytes = {0x02, command, static_cast<uint8_t>(data.size() + 2),
                                static_cast<uint8_t>(address >> 8), static_cast<uint8_t>(address & 0xFF)};
  bytes.insert(bytes.end(), data.begin(), data.end());
  bytes.push_back(frame_checksum(bytes.data() + 1, bytes.size() - 1));
  return bytes;
}

std::vector<uint8_t> reply(uint16_t address, const std::vector<uint8_t> &data) { return frame(0x06, address, data); }

uint16_t address_of(const std::array<uint8_t, 6> &request) {
  return static_cast<uint16_t>(request[3] << 8 | request[4]);
}

// A Session built from Register map rows, driven the way the hub's loop does with a fake
// millisecond clock.
struct Bus {
  explicit Bus(const std::vector<register_map::Row> &rows, uint32_t start = 0) : rows(rows), now(start) {
    for (const register_map::Row &row : rows)
      session.add_value(row.group, row.registration);
  }

  std::vector<register_map::Row> rows;
  Session session;
  uint32_t now;

  // The Address of the Read request the Session sends now, or 0xFFFF for none.
  uint32_t request(SessionOutput *out = nullptr) {
    std::array<uint8_t, 6> request;
    SessionOutput output;
    const bool send = session.next_request(now, request, output);
    if (out)
      *out = output;
    if (!send)
      return 0xFFFF;
    return address_of(request);
  }

  // Receives a Frame in one piece and returns each Value it published, by key.
  std::map<std::string, float> receive(const std::vector<uint8_t> &bytes, SessionOutput *out = nullptr) {
    SessionOutput output = session.feed(bytes.data(), bytes.size(), now);
    std::map<std::string, float> published;
    for (const auto &value : output.values)
      published[rows.at(value.index).key] = value.value;
    if (out)
      *out = output;
    return published;
  }

  void advance(uint32_t ms) { now += ms; }

  // Runs the loop with a silent Controller until `until`, a millisecond on the fake clock, and
  // returns what the Session reported meanwhile.
  SessionOutput run_silent(uint32_t until) {
    SessionOutput all;
    for (; now < until; advance(1)) {
      SessionOutput output;
      request(&output);
      all.missed.insert(all.missed.end(), output.missed.begin(), output.missed.end());
      all.stale.insert(all.stale.end(), output.stale.begin(), output.stale.end());
    }
    return all;
  }
};

// A Session's counts in the order of COUNTER_FIELDS, so one CHECK shows them all: Checksum
// failures, discarded bytes, retries, give-ups, Replies that decoded nothing.
std::vector<uint32_t> counts(const Counters &counters) {
  std::vector<uint32_t> out;
  for (const CounterField &field : COUNTER_FIELDS)
    out.push_back(counters.*field.count);
  return out;
}

std::vector<uint32_t> counts(const Session &session) { return counts(session.counters()); }

const std::vector<uint32_t> NO_ERRORS = {0, 0, 0, 0, 0};

}  // namespace

TEST_CASE("counters: a Reply with a bad Checksum counts a Checksum failure, and its bytes as discarded") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  std::vector<uint8_t> bytes = reply(0x12, {0xFE, 0x0C});
  bytes.back() ^= 0xFF;
  REQUIRE(bytes.size() == 8);
  CHECK(bus.receive(bytes).empty());
  CHECK(counts(bus.session) == std::vector<uint32_t>{1, 8, 0, 0, 0});
}

TEST_CASE("counters: since() gives the counts after an earlier reading, and any() whether one is non-zero") {
  Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
  const Counters start = bus.session.counters();
  CHECK_FALSE(start.any());

  CHECK(bus.request() == 0x12);
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0x12);
  const Counters first = bus.session.counters();
  CHECK(first.since(start).any());
  CHECK_FALSE(first.since(first).any());

  // Reading the counts doesn't reset them.
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 1, 0, 0});

  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0xFFFF);
  std::vector<uint8_t> bytes = reply(0x21, {0x14, 0x7E});
  bytes.back() ^= 0xFF;
  bus.receive(bytes);
  const Counters second = bus.session.counters();
  CHECK(counts(second.since(first)) == std::vector<uint32_t>{1, 8, 0, 1, 0});
  CHECK(counts(second.since(start)) == std::vector<uint32_t>{1, 8, 1, 1, 0});
}

TEST_CASE("counters: since() and any() cover every count") {
  for (const CounterField &field : COUNTER_FIELDS) {
    CAPTURE(field.label);
    Counters earlier;
    Counters later;
    later.*field.count = 2;
    CHECK(later.any());
    CHECK(later.since(earlier).*field.count == 2);
    CHECK_FALSE(later.since(later).any());
  }
}

TEST_CASE("counters: describe() names every count, in a line for the log") {
  Counters counters;
  counters.checksum_failures = 1;
  counters.discarded_bytes = 8;
  counters.retries = 1;
  counters.give_ups = 1;
  CHECK(counters.describe() ==
        "checksum failures 1, discarded bytes 8, retries 1, give-ups 1, replies that decoded nothing 0");
}

TEST_CASE("counters: since() is right across a count wrapping at 2^32") {
  Counters earlier;
  earlier.retries = UINT32_MAX;
  Counters later;
  later.retries = 2;
  CHECK(later.since(earlier).retries == 3);
}

TEST_CASE("bus error report: once per interval, with the counts and the time since the last line, and only when there are any") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  BusErrorReport report;
  Counters errors;
  uint32_t span_ms = 0;
  auto take = [&]() { return report.take(bus.now, 60000, bus.session.counters(), errors, span_ms); };

  // A Checksum failure and a timeout early in the first interval.
  std::vector<uint8_t> bad = reply(0x12, {0xFE, 0x0C});
  bad.back() ^= 0xFF;
  bus.receive(bad);
  CHECK(bus.request() == 0x12);
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0x12);
  CHECK_FALSE(take());

  bus.now = 59999;
  CHECK_FALSE(take());
  bus.now = 60000;
  REQUIRE(take());
  CHECK(counts(errors) == std::vector<uint32_t>{1, 8, 1, 0, 0});
  CHECK(span_ms == 60000);

  // An error right after a line waits for the next interval. A loop that runs late
  // stretches the span.
  bus.receive(bad);
  bus.advance(1);
  CHECK_FALSE(take());
  bus.now = 120007;
  REQUIRE(take());
  CHECK(counts(errors) == std::vector<uint32_t>{1, 8, 0, 0, 0});
  CHECK(span_ms == 60007);

  // An interval with no errors logs nothing.
  bus.now = 180007;
  CHECK_FALSE(take());

  // The quiet interval moved the next check on, so an error now waits for it, and the
  // line's span runs from the last line.
  bus.receive(bad);
  bus.now = 240006;
  CHECK_FALSE(take());
  bus.now = 240007;
  REQUIRE(take());
  CHECK(counts(errors) == std::vector<uint32_t>{1, 8, 0, 0, 0});
  CHECK(span_ms == 120000);
}

TEST_CASE("bus error report: the interval passed on each call sets the cadence") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  BusErrorReport report;
  Counters errors;
  uint32_t span_ms = 0;
  std::vector<uint8_t> bad = reply(0x12, {0xFE, 0x0C});
  bad.back() ^= 0xFF;
  bus.receive(bad);
  CHECK_FALSE(report.take(9999, 10000, bus.session.counters(), errors, span_ms));
  CHECK(report.take(10000, 10000, bus.session.counters(), errors, span_ms));
  CHECK(span_ms == 10000);
}

TEST_CASE("counters: a partial Frame dropped after a silence counts its bytes as discarded") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  const auto bytes = reply(0x12, {0xFE, 0x0C});
  bus.receive({bytes.begin(), bytes.begin() + 4});
  CHECK(counts(bus.session) == NO_ERRORS);
  bus.advance(SILENCE_GAP_MS + 1);
  CHECK(bus.receive(bytes).size() == 1);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 4, 0, 0, 0});
}

TEST_CASE("counters: bytes before a start byte are discarded") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  std::vector<uint8_t> bytes = {0x00, 0xFF, 0x58};
  const auto good = reply(0x12, {0xFE, 0x0C});
  bytes.insert(bytes.end(), good.begin(), good.end());
  CHECK(bus.receive(bytes).size() == 1);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 3, 0, 0, 0});
}

TEST_CASE("counters: a timeout counts a retry, and a second one a give-up") {
  Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
  CHECK(bus.request() == 0x12);
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0x12);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 1, 0, 0});
  CHECK(bus.session.counters().timeouts() == 1);
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0xFFFF);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 1, 1, 0});
  CHECK(bus.session.counters().timeouts() == 2);
}

TEST_CASE("a give-up reports its Address as missed from the request path, since no bytes arrive to feed") {
  Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
  SessionOutput output;
  CHECK(bus.request(&output) == 0x12);
  CHECK(output.missed.empty());
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request(&output) == 0x12);  // the retry is not a miss yet
  CHECK(output.missed.empty());
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request(&output) == 0xFFFF);
  CHECK(output.missed == std::vector<uint16_t>{0x12});
  // The miss was reported once.
  bus.advance(REQUEST_GAP_MS);
  CHECK(bus.request(&output) == 0x21);
  CHECK(output.missed.empty());
}

TEST_CASE("an Address goes stale after two missed cycles, once, with every entry registered at it") {
  // Entries 0, 1 and 2. The Status word and its compressor bit share Address 0x2D.
  Bus bus(register_map::rows_named({"outside_temp", "status_word", "compressor"}));
  const uint32_t cycle = esphome::geopro_202s::DEFAULT_VALUE_INTERVAL_MS;

  // Cycle 1: each Address is given up once, and nothing is stale yet.
  SessionOutput output = bus.run_silent(cycle);
  CHECK(output.missed == std::vector<uint16_t>{0x12, STATUS_WORD});
  CHECK(output.stale.empty());

  // Cycle 2: the second miss makes each Address stale, with every entry at it.
  output = bus.run_silent(2 * cycle);
  CHECK(output.missed == std::vector<uint16_t>{0x12, STATUS_WORD});
  CHECK(output.stale == std::vector<EntryId>{0, 1, 2});

  // Cycle 3: a stale Address is reported once, not on every further miss.
  output = bus.run_silent(3 * cycle);
  CHECK(output.missed == std::vector<uint16_t>{0x12, STATUS_WORD});
  CHECK(output.stale.empty());

  // Cycle 4: a Reply for 0x12 ends its run of misses; its Value restores the entry.
  REQUIRE(bus.request() == 0x12);
  CHECK(bus.receive(reply(0x12, {0xFE, 0x0C})) == std::map<std::string, float>{{"outside_temp", -5.0f}});
  output = bus.run_silent(4 * cycle);
  CHECK(output.missed == std::vector<uint16_t>{STATUS_WORD});
  CHECK(output.stale.empty());

  // Cycle 5: one miss since the Reply doesn't make 0x12 stale.
  output = bus.run_silent(5 * cycle);
  CHECK(output.missed == std::vector<uint16_t>{0x12, STATUS_WORD});
  CHECK(output.stale.empty());

  // Cycle 6: the second does, again.
  output = bus.run_silent(6 * cycle);
  CHECK(output.stale == std::vector<EntryId>{0});
}

TEST_CASE("a Reply that decodes nothing still answers, so it doesn't count towards staleness") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  const uint32_t cycle = esphome::geopro_202s::DEFAULT_VALUE_INTERVAL_MS;
  CHECK(bus.run_silent(cycle).missed == std::vector<uint16_t>{0x12});

  // Cycle 2 is answered with a Reply one data byte short, which decodes nothing.
  REQUIRE(bus.request() == 0x12);
  SessionOutput output;
  CHECK(bus.receive(reply(0x12, {0xFE}), &output).empty());
  CHECK(output.answered == std::vector<uint16_t>{0x12});

  // The run of misses starts over: cycle 3 is the first miss and cycle 4 the second.
  output = bus.run_silent(3 * cycle);
  CHECK(output.missed == std::vector<uint16_t>{0x12});
  CHECK(output.stale.empty());
  output = bus.run_silent(4 * cycle);
  CHECK(output.stale == std::vector<EntryId>{0});
}

TEST_CASE("a Reply for an Address nobody registered changes nothing") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  const uint32_t cycle = esphome::geopro_202s::DEFAULT_VALUE_INTERVAL_MS;
  CHECK(bus.run_silent(cycle).missed == std::vector<uint16_t>{0x12});
  SessionOutput output;
  bus.receive(reply(0x21, {0x14, 0x7E}), &output);
  CHECK(output.answered == std::vector<uint16_t>{0x21});
  CHECK(bus.run_silent(2 * cycle).stale == std::vector<EntryId>{0});
}

TEST_CASE("add_value gives ids counting up from 0, and the Session keeps the registrations") {
  const auto rows = register_map::rows_named({"outside_temp", "tank_top"});
  Session session;
  CHECK(session.add_value(rows[0].group, rows[0].registration) == EntryId(0));
  CHECK(session.add_value(rows[1].group, rows[1].registration) == EntryId(1));
  REQUIRE(session.registrations().size() == 2);
  CHECK(session.registrations()[1].address == rows[1].registration.address);
}

TEST_CASE("a Reply for the in-flight Address publishes its Value and completes the request") {
  Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
  CHECK(bus.request() == 0x12);

  bus.advance(100);
  SessionOutput output;
  auto published = bus.receive(reply(0x12, {0xFE, 0x0C}), &output);
  CHECK(published == std::map<std::string, float>{{"outside_temp", -5.0f}});
  CHECK(output.answered == std::vector<uint16_t>{0x12});

  // The next request waits out the gap after the Reply.
  bus.advance(REQUEST_GAP_MS - 1);
  CHECK(bus.request() == 0xFFFF);
  bus.advance(1);
  CHECK(bus.request() == 0x21);
}

TEST_CASE("a Frame with a Command byte other than 0x06 is not a Reply, with or without data") {
  // The Node's own Read request echoed back on the bus, and stand-ins for a write
  // acknowledgement or an error Frame, which would carry data.
  const std::vector<std::vector<uint8_t>> frames = {
      frame(0x81, 0x12, {}),
      frame(0x00, 0x12, {0xFE, 0x0C}),
      frame(0x15, 0x12, {0xFE, 0x0C}),
      frame(0x81, 0x12, {0xFE, 0x0C}),
  };
  for (const std::vector<uint8_t> &bytes : frames) {
    const uint8_t command = bytes[1], length = bytes[2];
    CAPTURE(command);
    CAPTURE(length);
    Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
    CHECK(bus.request() == 0x12);
    SessionOutput output;
    bus.receive(bytes, &output);
    CHECK(output.answered.empty());
    CHECK(output.values.empty());
    // A well-formed Frame that isn't a Reply is no bus error.
    CHECK(counts(bus.session) == NO_ERRORS);

    // The request is still in flight, so tank_top waits.
    bus.advance(REQUEST_GAP_MS);
    CHECK(bus.request() == 0xFFFF);
  }
}

TEST_CASE("a Reply for another Address publishes but does not complete the request") {
  Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
  CHECK(bus.request() == 0x12);
  bus.advance(10);
  auto published = bus.receive(reply(0x21, {0x14, 0x7E}));
  CHECK(published.count("tank_top") == 1);
  bus.advance(REQUEST_GAP_MS);
  CHECK(bus.request() == 0xFFFF);
}

TEST_CASE("a Reply that decodes nothing still completes the request, and counts as an error") {
  // A Bank Address answered with the wrong data length.
  Bus bus(register_map::rows_named({"comp_lock", "outside_temp"}));
  const uint32_t first = bus.request();
  REQUIRE(first == 0x12);
  bus.advance(10);
  bus.receive(reply(0x12, {0xFE, 0x0C}));
  bus.advance(REQUEST_GAP_MS);
  REQUIRE(bus.request() == 0x0B);
  bus.advance(10);
  SessionOutput output;
  bus.receive(reply(0x0B, {0x00, 0x01}), &output);
  CHECK(output.answered == std::vector<uint16_t>{0x0B});
  CHECK(output.values.empty());
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 0, 0, 1});

  // It answered the request, so it never times out.
  bus.advance(REPLY_TIMEOUT_MS * 2);
  CHECK(bus.request() == 0xFFFF);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 0, 0, 1});
}

TEST_CASE("a silent Controller gets a retry and then the next Address") {
  Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
  CHECK(bus.request() == 0x12);
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0x12);  // the retry
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0xFFFF);  // gives up and waits out the gap
  bus.advance(REQUEST_GAP_MS);
  CHECK(bus.request() == 0x21);
}

TEST_CASE("a Frame split across feeds is decoded when it completes") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  const auto bytes = reply(0x12, {0xFE, 0x0C});
  CHECK(bus.receive({bytes.begin(), bytes.begin() + 4}).empty());
  CHECK(bus.receive({bytes.begin() + 4, bytes.end()}) == std::map<std::string, float>{{"outside_temp", -5.0f}});
}

TEST_CASE("a partial Frame is kept when the rest arrives within the silence gap") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  const auto bytes = reply(0x12, {0xFE, 0x0C});
  CHECK(bus.receive({bytes.begin(), bytes.begin() + 4}).empty());
  bus.advance(SILENCE_GAP_MS);
  CHECK(bus.receive({bytes.begin() + 4, bytes.end()}) == std::map<std::string, float>{{"outside_temp", -5.0f}});
}

TEST_CASE("a partial Frame is dropped when the silence gap passes before the rest arrives") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  const auto bytes = reply(0x12, {0xFE, 0x0C});
  CHECK(bus.receive({bytes.begin(), bytes.begin() + 4}).empty());
  bus.advance(SILENCE_GAP_MS + 1);
  CHECK(bus.receive({bytes.begin() + 4, bytes.end()}).empty());

  // A whole Frame after it decodes.
  CHECK(bus.receive(bytes) == std::map<std::string, float>{{"outside_temp", -5.0f}});
}

TEST_CASE("a feed with no bytes doesn't end the silence") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  const auto bytes = reply(0x12, {0xFE, 0x0C});
  CHECK(bus.receive({bytes.begin(), bytes.begin() + 4}).empty());
  bus.advance(SILENCE_GAP_MS);
  CHECK(bus.receive({}).empty());
  bus.advance(1);
  CHECK(bus.receive({bytes.begin() + 4, bytes.end()}).empty());
}

TEST_CASE("status bits are read and published without the status-word sensor") {
  // Only the bit rows registered, as when status_word is left out of the config.
  std::vector<register_map::Row> rows;
  for (const register_map::Row &row : register_map::rows_at(STATUS_WORD))
    if (row.registration.rule.mask != 0)
      rows.push_back(row);
  Bus bus(rows);
  CHECK(bus.request() == STATUS_WORD);

  // compressor and digi2 on.
  const std::map<std::string, float> expected = {
      {"compressor", 1}, {"el_heater", 0}, {"digi1", 0}, {"digi2", 1}, {"digi3", 0},
  };
  CHECK(bus.receive(reply(STATUS_WORD, {0x00, 0x12})) == expected);
}

TEST_CASE("rows sharing an Address are requested once and publish from one Reply") {
  Bus bus(register_map::rows_named(
      {"outside_temp", "status_word", "compressor", "el_heater", "digi1", "digi2", "digi3"}));

  // Run one cycle, answering each request at once.
  std::vector<uint32_t> sent;
  std::map<std::string, float> published;
  for (; bus.now < 1000; bus.advance(1)) {
    const uint32_t address = bus.request();
    if (address == 0xFFFF)
      continue;
    sent.push_back(address);
    if (address == STATUS_WORD)
      published = bus.receive(reply(STATUS_WORD, {0x80, 0x19}));
    else
      bus.receive(reply(static_cast<uint16_t>(address), {0x00, 0x00}));
  }
  CHECK(sent == std::vector<uint32_t>{0x12, STATUS_WORD});

  // One Status word Reply feeds the word and all five bits, and nothing else.
  const std::map<std::string, float> expected = {
      {"status_word", 0x8019}, {"compressor", 1}, {"el_heater", 1}, {"digi1", 1}, {"digi2", 0}, {"digi3", 0},
  };
  CHECK(published == expected);
}

TEST_CASE("a Bank row moved to the value cadence still publishes") {
  // comp_lock as the Register map has it, but read every value interval.
  register_map::Row row = register_map::rows_named({"comp_lock"})[0];
  row.group = PollGroup::VALUE;
  Bus bus({row});
  CHECK(bus.request() == 0x0B);

  // The Reply is still a full Bank, with comp_lock at offset 14.
  std::vector<uint8_t> data(31, 0x00);
  data[14] = 0xFB;
  CHECK(bus.receive(reply(0x0B, data)) == std::map<std::string, float>{{"comp_lock", -5}});
}

TEST_CASE("the Session's bank interval is the scheduler's, which the hub's bus error report reads") {
  Session session;
  CHECK(session.bank_interval() == DEFAULT_BANK_INTERVAL_MS);
  session.set_bank_interval(30000);
  CHECK(session.bank_interval() == 30000);
}

TEST_CASE("the intervals set on the Session reach the scheduler") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  bus.session.set_value_interval(3000);
  CHECK(bus.request() == 0x12);
  bus.receive(reply(0x12, {0x00, 0x00}));
  bus.advance(2999);
  CHECK(bus.request() == 0xFFFF);
  bus.advance(1);
  CHECK(bus.request() == 0x12);
}
