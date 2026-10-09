#include "doctest.h"

#include "frame.h"

#include <vector>

using esphome::geopro_202s::build_read_request;
using esphome::geopro_202s::Frame;
using esphome::geopro_202s::FrameDecoder;

namespace {

std::vector<Frame> feed(FrameDecoder &decoder, const std::vector<uint8_t> &bytes) {
  return decoder.feed(bytes.data(), bytes.size());
}

// Replies carry Command byte 0x06, as in tests/traces/node-2026-10-09.log.
// 5.00 °C (raw 0x01F4) from address 0x0001
const std::vector<uint8_t> TEMP_5_00 = {0x02, 0x06, 0x04, 0x00, 0x01, 0x01, 0xF4, 0x00};
// 6.00 °C (raw 0x0258) from address 0x0001
const std::vector<uint8_t> TEMP_6_00 = {0x02, 0x06, 0x04, 0x00, 0x01, 0x02, 0x58, 0x65};

void check_temp_5_00(const std::vector<Frame> &frames) {
  REQUIRE(frames.size() == 1);
  CHECK(frames[0].command == 0x06);
  CHECK(frames[0].address == 0x0001);
  CHECK(frames[0].data == std::vector<uint8_t>{0x01, 0xF4});
}

}  // namespace

TEST_CASE("read request for an address") {
  auto request = build_read_request(0x002D);
  CHECK(std::vector<uint8_t>(request.begin(), request.end()) ==
        std::vector<uint8_t>{0x02, 0x81, 0x02, 0x00, 0x2D, 0xB0});

  auto high = build_read_request(0x01FF);
  CHECK(std::vector<uint8_t>(high.begin(), high.end()) == std::vector<uint8_t>{0x02, 0x81, 0x02, 0x01, 0xFF, 0x83});
}

TEST_CASE("frame split across several feeds") {
  FrameDecoder decoder;
  CHECK(feed(decoder, {0x02, 0x06}).empty());
  CHECK(feed(decoder, {0x04, 0x00, 0x01}).empty());
  CHECK(feed(decoder, {0x01, 0xF4}).empty());
  check_temp_5_00(feed(decoder, {0x00}));
}

TEST_CASE("temperature reply whose data contains 0x02") {
  FrameDecoder decoder;
  auto frames = feed(decoder, TEMP_6_00);
  REQUIRE(frames.size() == 1);
  CHECK(frames[0].address == 0x0001);
  CHECK(frames[0].data == std::vector<uint8_t>{0x02, 0x58});
}

TEST_CASE("bank reply holding values of 2") {
  std::vector<uint8_t> data = {0x1E, 0x16, 0x0E, 0x0A, 0x32, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00,
                               0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  REQUIRE(data.size() == 31);
  std::vector<uint8_t> reply = {0x02, 0x06, 0x21, 0x00, 0x0C};
  reply.insert(reply.end(), data.begin(), data.end());
  reply.push_back(0xB9);

  FrameDecoder decoder;
  auto frames = feed(decoder, reply);
  REQUIRE(frames.size() == 1);
  CHECK(frames[0].address == 0x000C);
  CHECK(frames[0].data == data);
}

TEST_CASE("bad checksum followed by a good frame") {
  FrameDecoder decoder;
  std::vector<uint8_t> bytes = {0x02, 0x06, 0x04, 0x00, 0x01, 0x02, 0x58, 0xFF};
  bytes.insert(bytes.end(), TEMP_5_00.begin(), TEMP_5_00.end());
  check_temp_5_00(feed(decoder, bytes));
}

TEST_CASE("good frame inside the span of a false start is still found") {
  FrameDecoder decoder;
  std::vector<uint8_t> bytes = {0x02, 0x06, 0x04, 0x00};
  bytes.insert(bytes.end(), TEMP_5_00.begin(), TEMP_5_00.end());
  check_temp_5_00(feed(decoder, bytes));
}

TEST_CASE("false start whose length byte is above 0x21") {
  FrameDecoder decoder;
  std::vector<uint8_t> bytes = {0x02, 0x06, 0x22};
  bytes.insert(bytes.end(), TEMP_5_00.begin(), TEMP_5_00.end());
  check_temp_5_00(feed(decoder, bytes));
}

TEST_CASE("length byte below 2") {
  for (uint8_t length : {0x00, 0x01}) {
    CAPTURE(length);
    FrameDecoder decoder;
    std::vector<uint8_t> bytes = {0x02, 0x06, length, 0x7F};
    bytes.insert(bytes.end(), TEMP_5_00.begin(), TEMP_5_00.end());
    check_temp_5_00(feed(decoder, bytes));
  }
}

TEST_CASE("bytes before the start byte are skipped") {
  FrameDecoder decoder;
  std::vector<uint8_t> bytes = {0x00, 0xFF, 0x58};
  bytes.insert(bytes.end(), TEMP_5_00.begin(), TEMP_5_00.end());
  check_temp_5_00(feed(decoder, bytes));
}

TEST_CASE("several frames in one feed") {
  FrameDecoder decoder;
  std::vector<uint8_t> bytes = TEMP_6_00;
  bytes.insert(bytes.end(), TEMP_5_00.begin(), TEMP_5_00.end());
  auto frames = feed(decoder, bytes);
  REQUIRE(frames.size() == 2);
  CHECK(frames[0].data == std::vector<uint8_t>{0x02, 0x58});
  CHECK(frames[1].data == std::vector<uint8_t>{0x01, 0xF4});
}
