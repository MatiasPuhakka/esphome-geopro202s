#include "doctest.h"

#include "frame.h"
#include "register_map.h"
#include "value_decoder.h"

#include <map>
#include <string>
#include <vector>

using esphome::geopro_202s::AddressKind;
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
const AddressKind SINGLE_VALUE = AddressKind::SINGLE_VALUE;
const AddressKind BANK = AddressKind::BANK;

// Wraps data bytes in a checksummed read reply from `address`.
std::vector<uint8_t> reply(uint16_t address, const std::vector<uint8_t> &data) {
  std::vector<uint8_t> bytes = {0x02, 0x06, static_cast<uint8_t>(data.size() + 2), static_cast<uint8_t>(address >> 8),
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
  // Every Register map row for Bank 0x0B. The data bytes below sit at offsets written out by
  // hand, so a row with a wrong offset decodes the wrong byte.
  const auto rows = register_map::rows_at(0x0B);
  const auto registrations = register_map::registrations(rows);

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
    decoded[rows.at(result.index).key] = result.value;

  const std::map<std::string, float> expected = {
      {"winter_temp", 55}, {"summer_temp", 50}, {"bottom_diff", 5}, {"top_diff", 3},     {"tank_min", 40},
      {"delay_time", 60},  {"top_eh_diff", 2},  {"extra_heating", 4}, {"extra_time", 12}, {"hp_mode", 1},
      {"brine_alert", -7}, {"dhw_pre", 20},     {"dhw_lock", 200},  {"comp_lock", -5},
  };
  CHECK(results.size() == registrations.size());
  CHECK(decoded == expected);
}

TEST_CASE("registration past the end of the data produces nothing") {
  const std::vector<Registration> registrations = {
      {0x0B, 30, S8, BANK}, {0x0B, 31, S8, BANK}, {0x0B, 30, {2, false}, BANK}};
  std::vector<uint8_t> data(31, 0x01);

  auto results = decode_values(0x0B, data, registrations);
  REQUIRE(results.size() == 1);
  CHECK(results[0].index == 0);
  CHECK(results[0].value == 1);
}

TEST_CASE("a reply with the wrong data length produces nothing") {
  // A Bank registration only decodes from a full Bank reply.
  CHECK(decode_values(0x0B, std::vector<uint8_t>(30, 0x01), {{0x0B, 1, S8, BANK}}).empty());
  CHECK(decode_values(0x0B, std::vector<uint8_t>(32, 0x01), {{0x0B, 1, S8, BANK}}).empty());
  // A single value only decodes from a reply exactly as long as the value.
  CHECK(decode_values(0x2D, {0x00, 0x10, 0x00}, {{0x2D, 0, {2, false}, SINGLE_VALUE}}).empty());
  CHECK(decode_values(0x31, {0x64, 0x00}, {{0x31, 0, U8, SINGLE_VALUE}}).empty());
}

TEST_CASE("registrations for other addresses are skipped") {
  const std::vector<Registration> registrations = {
      {0x0C, 0, S8, SINGLE_VALUE}, {0x0B, 0, S8, SINGLE_VALUE}, {0x2C, 0, S8, SINGLE_VALUE}};
  auto results = decode_values(0x0B, {0x80}, registrations);
  REQUIRE(results.size() == 1);
  CHECK(results[0].index == 1);
  CHECK(results[0].value == -128);
}

TEST_CASE("two-byte values are big-endian") {
  const std::vector<Registration> registrations = {{0x12, 0, {2, true}, SINGLE_VALUE},
                                                   {0x3A, 0, {2, false}, SINGLE_VALUE}};
  auto signed_results = decode_values(0x12, {0xFE, 0x0C}, registrations);
  REQUIRE(signed_results.size() == 1);
  CHECK(signed_results[0].value == -500);

  auto unsigned_results = decode_values(0x3A, {0xFE, 0x0C}, registrations);
  REQUIRE(unsigned_results.size() == 1);
  CHECK(unsigned_results[0].value == 65036);
}

namespace {

// Decode rules for the decode-math tests below.
const DecodeRule CENTI_S16 = {2, true, 100};
const DecodeRule U16 = {2, false};

const uint16_t STATUS_WORD = 0x2D;

float decode_single(uint16_t address, const std::vector<uint8_t> &data, DecodeRule rule) {
  const std::vector<Registration> registrations = {{address, 0, rule, SINGLE_VALUE}};
  Frame frame = receive(reply(address, data));
  auto results = decode_values(frame.address, frame.data, registrations);
  REQUIRE(results.size() == 1);
  return results[0].value;
}

// The Register map's Status bits: every row on the Status word with a mask.
std::vector<register_map::Row> status_bit_rows() {
  std::vector<register_map::Row> rows;
  for (const register_map::Row &row : register_map::rows_at(STATUS_WORD))
    if (row.registration.rule.mask != 0)
      rows.push_back(row);
  return rows;
}

// Decodes a Reply from `address` with `rows` and returns each decoded Value by key.
std::map<std::string, float> decode_rows(uint16_t address, const std::vector<uint8_t> &data,
                                         const std::vector<register_map::Row> &rows) {
  Frame frame = receive(reply(address, data));
  std::map<std::string, float> decoded;
  for (const DecodedValue &result : decode_values(frame.address, frame.data, register_map::registrations(rows)))
    decoded[rows.at(result.index).key] = result.value;
  return decoded;
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

TEST_CASE("every status bit decodes its own bit of the status word") {
  // The bit each Status bit reports, written out by hand to check the masks in register_map.py.
  const std::map<std::string, uint8_t> masks = {
      {"compressor", 0x10}, {"el_heater", 0x08}, {"digi1", 0x01}, {"digi2", 0x02}, {"digi3", 0x04},
  };
  const auto rows = status_bit_rows();
  for (const auto &bit : masks) {
    CAPTURE(bit.first);
    std::map<std::string, float> only_this, all_but_this;
    for (const auto &other : masks) {
      only_this[other.first] = other.first == bit.first;
      all_but_this[other.first] = other.first != bit.first;
    }
    // Only this bit set, then every bit but this one.
    CHECK(decode_rows(STATUS_WORD, {0x00, bit.second}, rows) == only_this);
    CHECK(decode_rows(STATUS_WORD, {0xFF, static_cast<uint8_t>(~bit.second)}, rows) == all_but_this);
  }
}

TEST_CASE("a zero divisor produces nothing") {
  CHECK(decode_values(0x12, {0x00, 0x01}, {{0x12, 0, {2, true, 0}, SINGLE_VALUE}}).empty());
}
