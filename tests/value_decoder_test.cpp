#include "doctest.h"

#include "frame.h"
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
