#include "doctest.h"

#include "frame.h"
#include "poll_scheduler.h"
#include "value_decoder.h"

#include <fstream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using esphome::geopro_202s::build_read_request;
using esphome::geopro_202s::decode_values;
using esphome::geopro_202s::DecodedValue;
using esphome::geopro_202s::DecodeRule;
using esphome::geopro_202s::Frame;
using esphome::geopro_202s::FrameDecoder;
using esphome::geopro_202s::PollGroup;
using esphome::geopro_202s::Registration;

// The Makefile passes the trace's absolute path, so the tests find it from any working directory.
#ifndef NODE_TRACE
#error "build with -DNODE_TRACE=\"<absolute path of tests/traces/node-2026-10-09.log>\""
#endif

namespace {

// One trace line: the bytes of a Read request the Node sent (">>>") or of a Reply it received ("<<<").
struct TraceLine {
  bool sent;
  std::vector<uint8_t> bytes;
};

std::vector<TraceLine> read_trace() {
  std::ifstream file(NODE_TRACE);
  REQUIRE_MESSAGE(file.is_open(), "can't open " NODE_TRACE);
  std::vector<TraceLine> lines;
  std::string text;
  while (std::getline(file, text)) {
    if (text.empty() || text[0] == '#')
      continue;
    size_t at = text.find(">>> ");
    const bool sent = at != std::string::npos;
    if (!sent)
      at = text.find("<<< ");
    REQUIRE_MESSAGE(at != std::string::npos, text);
    TraceLine line{sent, {}};
    std::istringstream hex(text.substr(at + 4));
    unsigned byte;
    while (hex >> std::hex >> byte)
      line.bytes.push_back(static_cast<uint8_t>(byte));
    lines.push_back(line);
  }
  return lines;
}

uint16_t requested_address(const TraceLine &request) {
  return static_cast<uint16_t>(request.bytes[3] << 8 | request.bytes[4]);
}

// Feeds a Reply to the decoder one byte at a time, as the Component reads the bus.
std::vector<Frame> receive(FrameDecoder &decoder, const TraceLine &reply) {
  std::vector<Frame> frames;
  for (uint8_t byte : reply.bytes)
    for (Frame &frame : decoder.feed(&byte, 1))
      frames.push_back(frame);
  return frames;
}

}  // namespace

TEST_CASE("node trace: the Node's Read requests are the ones build_read_request() makes") {
  auto lines = read_trace();
  REQUIRE(lines.size() == 34);
  for (const TraceLine &line : lines) {
    if (!line.sent)
      continue;
    REQUIRE(line.bytes.size() == 6);
    auto request = build_read_request(requested_address(line));
    CHECK(line.bytes == std::vector<uint8_t>(request.begin(), request.end()));
  }
}

TEST_CASE("node trace: each Reply is one Frame for the requested Address, with Command byte 0x06") {
  FrameDecoder decoder;
  uint16_t requested = 0;
  size_t replies = 0;
  size_t replies_with_0x02_inside = 0;
  for (const TraceLine &line : read_trace()) {
    if (line.sent) {
      requested = requested_address(line);
      continue;
    }
    CAPTURE(requested);
    auto frames = receive(decoder, line);
    REQUIRE(frames.size() == 1);
    CHECK(frames[0].command == 0x06);
    CHECK(frames[0].address == requested);
    // 0x02 is never escaped: a Reply is Length byte + 4 bytes even with 0x02 inside it.
    CHECK(line.bytes.size() == line.bytes[2] + 4u);
    for (size_t i = 1; i < line.bytes.size(); i++) {
      if (line.bytes[i] == 0x02) {
        replies_with_0x02_inside++;
        break;
      }
    }
    replies++;
  }
  CHECK(replies == 17);
  // Banks 0x0C and 0x0B, whose data holds a 2 (offsets 19 and 9).
  CHECK(replies_with_0x02_inside == 2);
}

TEST_CASE("node trace: Values decode to what the Node published") {
  // Rows as in register_map.py. Expected numbers are what the Node published in the same minute.
  const DecodeRule CENTI_S16 = {2, true, 100};
  const DecodeRule S8 = {1, true};
  const DecodeRule U8 = {1, false};
  const DecodeRule U16 = {2, false};
  const PollGroup VALUE = PollGroup::VALUE;
  const PollGroup BANK = PollGroup::BANK;
  const std::vector<std::pair<std::string, Registration>> rows = {
      {"outside_temp", {0x12, 0, CENTI_S16, VALUE}},
      {"tank_top_in", {0x18, 0, CENTI_S16, VALUE}},
      {"tank_bottom", {0x22, 0, CENTI_S16, VALUE}},
      {"brine", {0x19, 0, CENTI_S16, VALUE}},
      {"valve_dhw", {0x33, 0, U8, VALUE}},
      {"hours_eh", {0x3A, 0, U16, VALUE}},
      {"hours_comp", {0x3B, 0, U16, VALUE}},
      {"status_word", {0x2D, 0, U16, VALUE}},
      {"compressor", {0x2D, 0, {2, false, 1, 0x10}, VALUE}},
      {"el_heater", {0x2D, 0, {2, false, 1, 0x08}, VALUE}},
      {"l1_minus20", {0x0C, 0, S8, BANK}},
      {"l1_out_temp_delay", {0x0C, 19, S8, BANK}},  // a raw 0x02 on the wire
      {"l1_pre_increase", {0x0C, 23, S8, BANK}},
      {"l1_summer_close", {0x2C, 8, S8, BANK}},
      {"extra_time", {0x0B, 9, S8, BANK}},  // a raw 0x02 on the wire
      {"brine_alert", {0x0B, 11, S8, BANK}},
      {"comp_lock", {0x0B, 14, S8, BANK}},
  };
  std::vector<Registration> registrations;
  for (const auto &row : rows)
    registrations.push_back(row.second);

  FrameDecoder decoder;
  std::map<std::string, float> decoded;
  for (const TraceLine &line : read_trace()) {
    if (line.sent)
      continue;
    for (const Frame &frame : receive(decoder, line))
      for (const DecodedValue &result : decode_values(frame.address, frame.data, registrations))
        decoded[rows[result.index].first] = result.value;
  }

  const std::map<std::string, float> expected = {
      {"outside_temp", 11.8f}, {"tank_top_in", 44.5f},    {"tank_bottom", 48.3f},   {"brine", 15.1f},
      {"valve_dhw", 0},        {"hours_eh", 7355},        {"hours_comp", 8193},     {"status_word", 65031},
      {"compressor", 0},       {"el_heater", 0},          {"l1_minus20", 36},       {"l1_out_temp_delay", 2},
      {"l1_pre_increase", 0},  {"l1_summer_close", 30},   {"extra_time", 2},        {"brine_alert", -6},
      {"comp_lock", 48},
  };
  REQUIRE(decoded.size() == expected.size());
  for (const auto &value : expected) {
    CAPTURE(value.first);
    CHECK(decoded.at(value.first) == doctest::Approx(value.second));
  }
}
