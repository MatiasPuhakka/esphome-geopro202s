#include "doctest.h"

#include "frame.h"
#include "poll_scheduler.h"
#include "register_map.h"
#include "session.h"

#include <array>
#include <map>
#include <string>
#include <vector>

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

}  // namespace

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

TEST_CASE("a Reply that decodes nothing still completes the request") {
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
