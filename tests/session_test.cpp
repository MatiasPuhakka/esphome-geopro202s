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
using esphome::geopro_202s::Counters;
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
  uint32_t request() {
    std::array<uint8_t, 6> request;
    if (!session.next_request(now, request))
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
};

// A Session's counts in a fixed order, so one CHECK shows them all: Checksum failures,
// discarded bytes, timeouts, retries, give-ups, Replies that decoded nothing.
std::vector<uint32_t> counts(const Counters &counters) {
  return {counters.checksum_failures, counters.discarded_bytes, counters.timeouts(),
          counters.retries,           counters.give_ups,        counters.undecoded_replies};
}

std::vector<uint32_t> counts(const Session &session) { return counts(session.counters()); }

const std::vector<uint32_t> NO_ERRORS = {0, 0, 0, 0, 0, 0};

}  // namespace

TEST_CASE("counters: a Reply with a bad Checksum counts a Checksum failure, and its bytes as discarded") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  std::vector<uint8_t> bytes = reply(0x12, {0xFE, 0x0C});
  bytes.back() ^= 0xFF;
  REQUIRE(bytes.size() == 8);
  CHECK(bus.receive(bytes).empty());
  CHECK(counts(bus.session) == std::vector<uint32_t>{1, 8, 0, 0, 0, 0});
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
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 1, 1, 0, 0});

  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0xFFFF);
  std::vector<uint8_t> bytes = reply(0x21, {0x14, 0x7E});
  bytes.back() ^= 0xFF;
  bus.receive(bytes);
  const Counters second = bus.session.counters();
  CHECK(counts(second.since(first)) == std::vector<uint32_t>{1, 8, 1, 0, 1, 0});
  CHECK(counts(second.since(start)) == std::vector<uint32_t>{1, 8, 2, 1, 1, 0});
}

TEST_CASE("counters: since() is right across a count wrapping at 2^32") {
  Counters earlier;
  earlier.retries = UINT32_MAX;
  Counters later;
  later.retries = 2;
  CHECK(later.since(earlier).retries == 3);
}

TEST_CASE("bus error report: once per interval, with the counts since the last one, and only when there are any") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  BusErrorReport report;
  report.set_interval(60000);
  Counters errors;

  // A Checksum failure and a timeout early in the first interval.
  std::vector<uint8_t> bad = reply(0x12, {0xFE, 0x0C});
  bad.back() ^= 0xFF;
  bus.receive(bad);
  CHECK(bus.request() == 0x12);
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0x12);
  CHECK_FALSE(report.take(bus.now, bus.session.counters(), errors));

  bus.now = 59999;
  CHECK_FALSE(report.take(bus.now, bus.session.counters(), errors));
  bus.now = 60000;
  REQUIRE(report.take(bus.now, bus.session.counters(), errors));
  CHECK(counts(errors) == std::vector<uint32_t>{1, 8, 1, 1, 0, 0});

  // An error right after a report waits for the next interval.
  bus.receive(bad);
  bus.advance(1);
  CHECK_FALSE(report.take(bus.now, bus.session.counters(), errors));
  bus.now = 120000;
  REQUIRE(report.take(bus.now, bus.session.counters(), errors));
  CHECK(counts(errors) == std::vector<uint32_t>{1, 8, 0, 0, 0, 0});

  // An interval with no errors reports nothing.
  bus.now = 180000;
  CHECK_FALSE(report.take(bus.now, bus.session.counters(), errors));

  // The quiet interval moved the report on, so an error now waits for the next one.
  bus.receive(bad);
  bus.now = 239999;
  CHECK_FALSE(report.take(bus.now, bus.session.counters(), errors));
  bus.now = 240000;
  REQUIRE(report.take(bus.now, bus.session.counters(), errors));
  CHECK(counts(errors) == std::vector<uint32_t>{1, 8, 0, 0, 0, 0});
}

TEST_CASE("counters: a partial Frame dropped after a silence counts its bytes as discarded") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  const auto bytes = reply(0x12, {0xFE, 0x0C});
  bus.receive({bytes.begin(), bytes.begin() + 4});
  CHECK(counts(bus.session) == NO_ERRORS);
  bus.advance(SILENCE_GAP_MS + 1);
  CHECK(bus.receive(bytes).size() == 1);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 4, 0, 0, 0, 0});
}

TEST_CASE("counters: bytes before a start byte are discarded") {
  Bus bus(register_map::rows_named({"outside_temp"}));
  CHECK(bus.request() == 0x12);
  std::vector<uint8_t> bytes = {0x00, 0xFF, 0x58};
  const auto good = reply(0x12, {0xFE, 0x0C});
  bytes.insert(bytes.end(), good.begin(), good.end());
  CHECK(bus.receive(bytes).size() == 1);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 3, 0, 0, 0, 0});
}

TEST_CASE("counters: a timeout counts a retry, and a second one a give-up") {
  Bus bus(register_map::rows_named({"outside_temp", "tank_top"}));
  CHECK(bus.request() == 0x12);
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0x12);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 1, 1, 0, 0});
  bus.advance(REPLY_TIMEOUT_MS);
  CHECK(bus.request() == 0xFFFF);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 2, 1, 1, 0});
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
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 0, 0, 0, 1});

  // It answered the request, so it never times out.
  bus.advance(REPLY_TIMEOUT_MS * 2);
  CHECK(bus.request() == 0xFFFF);
  CHECK(counts(bus.session) == std::vector<uint32_t>{0, 0, 0, 0, 0, 1});
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
