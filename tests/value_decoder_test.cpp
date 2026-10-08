#include "doctest.h"

#include "frame.h"
#include "poll_scheduler.h"
#include "value_decoder.h"

#include <map>
#include <string>
#include <vector>

using esphome::geopro_202s::decode_values;
using esphome::geopro_202s::DecodedValue;
using esphome::geopro_202s::DecodeRule;
using esphome::geopro_202s::Frame;
using esphome::geopro_202s::FrameDecoder;
using esphome::geopro_202s::frame_checksum;
using esphome::geopro_202s::PollScheduler;
using esphome::geopro_202s::Registration;

namespace {

const DecodeRule S8 = {1, true};
const DecodeRule U8 = {1, false};

// Wraps data bytes in a checksummed read reply from `address`.
std::vector<uint8_t> reply(uint16_t address, const std::vector<uint8_t> &data) {
  std::vector<uint8_t> bytes = {0x02, 0x81, static_cast<uint8_t>(data.size() + 2), static_cast<uint8_t>(address >> 8),
                                static_cast<uint8_t>(address & 0xFF)};
  bytes.insert(bytes.end(), data.begin(), data.end());
  bytes.push_back(frame_checksum(bytes.data() + 1, bytes.size() - 1));
  return bytes;
}

Frame receive(const std::vector<uint8_t> &bytes) {
  FrameDecoder decoder;
  auto frames = decoder.feed(bytes.data(), bytes.size());
  REQUIRE(frames.size() == 1);
  return frames[0];
}

}  // namespace

TEST_CASE("full bank 0x0B frame decodes every key") {
  // Bank 0x0B rows from value_table.py.
  const std::vector<std::string> keys = {
      "winter_temp", "summer_temp",   "bottom_diff", "top_diff", "tank_min", "delay_time", "top_eh_diff",
      "extra_heating", "extra_time", "hp_mode",     "brine_alert", "dhw_pre", "dhw_lock",  "comp_lock",
  };
  const std::vector<Registration> registrations = {
      {0x0B, 1, S8},  {0x0B, 2, S8},  {0x0B, 3, S8},  {0x0B, 4, S8},  {0x0B, 5, S8},
      {0x0B, 6, S8},  {0x0B, 7, S8},  {0x0B, 8, S8},  {0x0B, 9, S8},  {0x0B, 10, S8},
      {0x0B, 11, S8}, {0x0B, 12, S8}, {0x0B, 13, U8}, {0x0B, 14, S8},
  };
  REQUIRE(keys.size() == registrations.size());

  std::vector<uint8_t> data(31, 0x00);
  data[1] = 55;    // winter_temp
  data[2] = 50;    // summer_temp
  data[3] = 5;     // bottom_diff
  data[4] = 3;     // top_diff
  data[5] = 40;    // tank_min
  data[6] = 60;    // delay_time
  data[7] = 2;     // top_eh_diff
  data[8] = 4;     // extra_heating
  data[9] = 12;    // extra_time
  data[10] = 1;    // hp_mode
  data[11] = 0xF9; // brine_alert, -7 °C
  data[12] = 20;   // dhw_pre
  data[13] = 0xC8; // dhw_lock, 200 s
  data[14] = 0xFB; // comp_lock, -5 °C

  Frame frame = receive(reply(0x0B, data));
  auto results = decode_values(frame.address, frame.data, registrations);

  std::map<std::string, float> decoded;
  for (const DecodedValue &result : results)
    decoded[keys.at(result.index)] = result.value;

  const std::map<std::string, float> expected = {
      {"winter_temp", 55}, {"summer_temp", 50}, {"bottom_diff", 5}, {"top_diff", 3},     {"tank_min", 40},
      {"delay_time", 60},  {"top_eh_diff", 2},  {"extra_heating", 4}, {"extra_time", 12}, {"hp_mode", 1},
      {"brine_alert", -7}, {"dhw_pre", 20},     {"dhw_lock", 200},  {"comp_lock", -5},
  };
  CHECK(results.size() == registrations.size());
  CHECK(decoded == expected);
}

TEST_CASE("registration past the end of the data produces nothing") {
  const std::vector<Registration> registrations = {{0x0B, 30, S8}, {0x0B, 31, S8}, {0x0B, 30, {2, false}}};
  std::vector<uint8_t> data(31, 0x01);

  auto results = decode_values(0x0B, data, registrations);
  REQUIRE(results.size() == 1);
  CHECK(results[0].index == 0);
  CHECK(results[0].value == 1);
}

TEST_CASE("registrations for other addresses are skipped") {
  const std::vector<Registration> registrations = {{0x0C, 0, S8}, {0x0B, 0, S8}, {0x2C, 0, S8}};
  auto results = decode_values(0x0B, {0x80}, registrations);
  REQUIRE(results.size() == 1);
  CHECK(results[0].index == 1);
  CHECK(results[0].value == -128);
}

TEST_CASE("two-byte values are big-endian") {
  const std::vector<Registration> registrations = {{0x12, 0, {2, true}}, {0x3A, 0, {2, false}}};
  auto signed_results = decode_values(0x12, {0xFE, 0x0C}, registrations);
  REQUIRE(signed_results.size() == 1);
  CHECK(signed_results[0].value == -500);

  auto unsigned_results = decode_values(0x3A, {0xFE, 0x0C}, registrations);
  REQUIRE(unsigned_results.size() == 1);
  CHECK(unsigned_results[0].value == 65036);
}

namespace {

// Decode rules as value_table.py builds them for single-address rows.
const DecodeRule CENTI_S16 = {2, true, 100};
const DecodeRule U16 = {2, false};
DecodeRule status_bit(uint16_t mask) { return DecodeRule(2, false, 1, mask); }

const uint16_t STATUS_WORD = 0x2D;

// The status-word bits in value_table.py.
struct StatusBit {
  const char *key;
  uint16_t mask;
};
const std::vector<StatusBit> STATUS_BITS = {
    {"compressor", 0x10}, {"el_heater", 0x08}, {"digi1", 0x01}, {"digi2", 0x02}, {"digi3", 0x04},
};

float decode_single(uint16_t address, const std::vector<uint8_t> &data, DecodeRule rule) {
  const std::vector<Registration> registrations = {{address, 0, rule}};
  Frame frame = receive(reply(address, data));
  auto results = decode_values(frame.address, frame.data, registrations);
  REQUIRE(results.size() == 1);
  return results[0].value;
}

}  // namespace

TEST_CASE("temperature is signed hundredths of a degree") {
  CHECK(decode_single(0x12, {0xFE, 0x0C}, CENTI_S16) == doctest::Approx(-5.0f));
  CHECK(decode_single(0x12, {0xFF, 0xF6}, CENTI_S16) == doctest::Approx(-0.1f));
  CHECK(decode_single(0x21, {0x14, 0x7E}, CENTI_S16) == doctest::Approx(52.46f));
}

TEST_CASE("valve position is one unsigned byte") {
  CHECK(decode_single(0x31, {0x64}, U8) == 100);
  CHECK(decode_single(0x33, {0xC8}, U8) == 200);
}

TEST_CASE("hour counter above 32767 stays positive") {
  CHECK(decode_single(0x3B, {0x9C, 0x40}, U16) == 40000);
  CHECK(decode_single(0x3A, {0xFF, 0xFF}, U16) == 65535);
}

TEST_CASE("every status bit decodes from the status word") {
  for (const StatusBit &bit : STATUS_BITS) {
    CAPTURE(bit.key);
    // Only this bit set, then every bit but this one.
    CHECK(decode_single(STATUS_WORD, {0x00, static_cast<uint8_t>(bit.mask)}, status_bit(bit.mask)) == 1);
    CHECK(decode_single(STATUS_WORD, {0xFF, static_cast<uint8_t>(~bit.mask)}, status_bit(bit.mask)) == 0);
  }
}

TEST_CASE("status bits are read and published without the status-word sensor") {
  // Only bit rows registered, as when status_word is left out of the config.
  std::vector<Registration> registrations;
  for (const StatusBit &bit : STATUS_BITS)
    registrations.push_back({STATUS_WORD, 0, status_bit(bit.mask)});

  PollScheduler scheduler;
  for (const Registration &registration : registrations)
    scheduler.add_value_address(registration.address);
  uint16_t address;
  REQUIRE(scheduler.next_request(0, address));
  CHECK(address == STATUS_WORD);

  // compressor and digi2 on.
  auto results = decode_values(STATUS_WORD, {0x00, 0x12}, registrations);
  REQUIRE(results.size() == STATUS_BITS.size());
  std::map<std::string, float> decoded;
  for (const DecodedValue &result : results)
    decoded[STATUS_BITS.at(result.index).key] = result.value;
  const std::map<std::string, float> expected = {
      {"compressor", 1}, {"el_heater", 0}, {"digi1", 0}, {"digi2", 1}, {"digi3", 0},
  };
  CHECK(decoded == expected);
}

TEST_CASE("rows sharing an address are requested once and decode from one reply") {
  // A temperature, the status-word sensor and every status bit, as the hub
  // registers them from the table.
  std::vector<Registration> registrations = {{0x12, 0, CENTI_S16}, {STATUS_WORD, 0, U16}};
  for (const StatusBit &bit : STATUS_BITS)
    registrations.push_back({STATUS_WORD, 0, status_bit(bit.mask)});

  PollScheduler scheduler;
  for (const Registration &registration : registrations)
    scheduler.add_value_address(registration.address);

  // Run one cycle, answering each request at once.
  std::vector<uint16_t> sent;
  for (uint32_t now = 0; now < 1000; now++) {
    uint16_t address;
    if (scheduler.next_request(now, address)) {
      sent.push_back(address);
      scheduler.on_frame(address, now);
    }
  }
  CHECK(sent == std::vector<uint16_t>{0x12, STATUS_WORD});

  // One status-word reply feeds the word and all five bits, and nothing else.
  Frame frame = receive(reply(STATUS_WORD, {0x80, 0x19}));
  auto results = decode_values(frame.address, frame.data, registrations);
  REQUIRE(results.size() == 1 + STATUS_BITS.size());
  CHECK(results[0].index == 1);
  CHECK(results[0].value == 0x8019);
  const std::vector<float> bits = {1, 1, 1, 0, 0};  // compressor, el_heater, digi1, digi2, digi3
  for (size_t i = 0; i < bits.size(); i++) {
    CHECK(results[i + 1].index == i + 2);
    CHECK(results[i + 1].value == bits[i]);
  }
}

TEST_CASE("a zero divisor produces nothing") {
  CHECK(decode_values(0x12, {0x00, 0x01}, {{0x12, 0, {2, true, 0}}}).empty());
}
