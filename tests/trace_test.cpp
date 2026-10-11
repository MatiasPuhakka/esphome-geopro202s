#include "doctest.h"

#include "frame.h"
#include "register_map.h"
#include "value_decoder.h"

#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using esphome::geopro_202s::build_read_request;
using esphome::geopro_202s::decode_values;
using esphome::geopro_202s::DecodedValue;
using esphome::geopro_202s::Frame;
using esphome::geopro_202s::FrameDecoder;

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

// A Value the trace should decode to, and the record it comes from.
struct ExpectedValue {
  float value;
  std::string source;
};

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

TEST_CASE("node trace: every row whose Address the trace covers decodes to its expected Value") {
  // Each expected Value names its source, so a failure shows whether Home Assistant or the hand
  // decode disagrees with the Register map.
  // The Value the Node published to Home Assistant: Home Assistant's history for each entity at
  // 2026-10-09 14:57:45 Finnish time (11:57:45 UTC), the second before this trace starts. Home
  // Assistant shows extra_time as 120 min; the Node published 2 h. All 24 Bank Values also
  // matched the Controller's display that day (#10).
  const std::string HOME_ASSISTANT = "Home Assistant";
  // Not published at the trace time, so decoded by hand from the trace bytes.
  const std::string HAND_DECODE = "hand decode";

  const std::map<std::string, ExpectedValue> expected = {
      // Measurements
      {"outside_temp", {11.8f, HOME_ASSISTANT}},
      {"l1_room", {0, HOME_ASSISTANT}},
      {"l1_supply", {23.8f, HOME_ASSISTANT}},
      {"free_measurement", {0, HOME_ASSISTANT}},
      {"tank_top_in", {44.5f, HOME_ASSISTANT}},
      {"tank_top", {49.4f, HOME_ASSISTANT}},
      {"tank_middle", {48.2f, HOME_ASSISTANT}},
      {"tank_bottom", {48.3f, HOME_ASSISTANT}},
      {"brine", {15.1f, HOME_ASSISTANT}},
      {"valve_l1", {0, HOME_ASSISTANT}},
      {"valve_dhw", {0, HOME_ASSISTANT}},
      {"hours_eh", {7355, HOME_ASSISTANT}},
      {"hours_comp", {8193, HOME_ASSISTANT}},
      {"status_word", {65031, HOME_ASSISTANT}},
      // Status bits. Home Assistant had compressor and el_heater off. The Node had no digi keys
      // configured, and the Status word's low byte, 0x07, sets all three of their bits.
      {"compressor", {0, HOME_ASSISTANT}},
      {"el_heater", {0, HOME_ASSISTANT}},
      {"digi1", {1, HAND_DECODE}},
      {"digi2", {1, HAND_DECODE}},
      {"digi3", {1, HAND_DECODE}},
      // Bank 0x0C
      {"l1_minus20", {36, HOME_ASSISTANT}},
      {"l1_zero", {29, HOME_ASSISTANT}},
      {"l1_plus20", {20, HOME_ASSISTANT}},
      {"l1_min_limit", {20, HOME_ASSISTANT}},
      {"l1_max_limit", {65, HOME_ASSISTANT}},
      {"l1_night_effect", {0, HOME_ASSISTANT}},
      {"l1_autumn_dry", {3, HOME_ASSISTANT}},
      {"l1_out_temp_delay", {2, HOME_ASSISTANT}},  // a raw 0x02 on the wire
      {"l1_pre_increase", {0, HOME_ASSISTANT}},
      // Bank 0x2C
      {"l1_summer_close", {30, HOME_ASSISTANT}},
      // Bank 0x0B
      {"winter_temp", {55, HOME_ASSISTANT}},
      {"summer_temp", {50, HOME_ASSISTANT}},
      {"bottom_diff", {5, HOME_ASSISTANT}},
      {"top_diff", {3, HOME_ASSISTANT}},
      {"tank_min", {32, HOME_ASSISTANT}},
      {"delay_time", {90, HOME_ASSISTANT}},
      {"top_eh_diff", {5, HOME_ASSISTANT}},
      {"extra_heating", {50, HOME_ASSISTANT}},
      {"extra_time", {2, HOME_ASSISTANT}},  // a raw 0x02 on the wire
      {"hp_mode", {0, HOME_ASSISTANT}},
      {"brine_alert", {-6, HOME_ASSISTANT}},
      {"dhw_pre", {40, HOME_ASSISTANT}},
      {"dhw_lock", {60, HOME_ASSISTANT}},
      {"comp_lock", {48, HOME_ASSISTANT}},
  };

  const auto &rows = register_map::all_rows();
  const auto registrations = register_map::registrations(rows);

  FrameDecoder decoder;
  std::set<uint16_t> replied_addresses;
  std::map<std::string, float> decoded;
  for (const TraceLine &line : read_trace()) {
    if (line.sent)
      continue;
    for (const Frame &frame : receive(decoder, line)) {
      replied_addresses.insert(frame.address);
      for (const DecodedValue &result : decode_values(frame.address, frame.data, registrations))
        decoded[rows[result.index].key] = result.value;
    }
  }

  size_t checked = 0;
  for (const register_map::Row &row : rows) {
    if (replied_addresses.count(row.registration.address) == 0)
      continue;
    CAPTURE(row.key);
    auto expected_value = expected.find(row.key);
    if (expected_value == expected.end()) {
      FAIL_CHECK("the trace has a Reply for this row's Address but the test has no expected Value for it");
      continue;
    }
    CAPTURE(expected_value->second.source);
    checked++;
    auto decoded_value = decoded.find(row.key);
    if (decoded_value == decoded.end()) {
      FAIL_CHECK("the row decoded to nothing");
      continue;
    }
    CHECK(decoded_value->second == doctest::Approx(expected_value->second.value));
  }
  // Every expected Value belongs to a row the trace covers, so a row that was renamed, removed or
  // moved to an Address outside the trace fails here.
  CHECK(checked == expected.size());
}
