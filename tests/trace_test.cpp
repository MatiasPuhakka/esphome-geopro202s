#include "doctest.h"

#include "frame.h"
#include "register_map.h"
#include "session.h"
#include "value_decoder.h"

#include <array>
#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using esphome::geopro_202s::build_read_request;
using esphome::geopro_202s::COUNTER_FIELDS;
using esphome::geopro_202s::CounterField;
using esphome::geopro_202s::Counters;
using esphome::geopro_202s::Frame;
using esphome::geopro_202s::FrameDecoder;
using esphome::geopro_202s::Session;
using esphome::geopro_202s::SessionOutput;

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

// The Addresses the trace has a Read request for.
std::set<uint16_t> traced_addresses() {
  std::set<uint16_t> traced;
  for (const TraceLine &line : read_trace())
    if (line.sent)
      traced.insert(requested_address(line));
  return traced;
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

// What a Session did while the trace's Replies played back.
struct Replay {
  std::vector<std::array<uint8_t, 6>> requests;
  std::vector<uint16_t> answered;
  std::map<std::string, float> published;  // by Register map key
  Counters counters;                       // at the end
};

// Plays the trace through a Session built from the real Register map rows, as the hub would:
// time advances in 5 ms steps, and each Read request the Session sends gets the trace's Reply
// for that Address, fed in one byte at a time 20 ms later. The Session asks in its own order,
// not the trace's, so Replies are matched by Address. `before` is fed at time 0, ahead of the
// first Read request. With `echo`, each Read request is also fed back as it is sent, as a
// Node that hears itself on the bus would receive it. Stops before the second cycle (10 s).
Replay replay_trace(const std::vector<register_map::Row> &rows, const std::vector<uint8_t> &before = {},
                    bool echo = false) {
  std::map<uint16_t, TraceLine> replies;
  uint16_t requested = 0;
  for (const TraceLine &line : read_trace()) {
    if (line.sent)
      requested = requested_address(line);
    else
      replies[requested] = line;
  }

  Session session;
  for (const register_map::Row &row : rows)
    session.add_value(row.group, row.registration);

  Replay replay;
  auto record = [&](const SessionOutput &output) {
    replay.answered.insert(replay.answered.end(), output.answered.begin(), output.answered.end());
    for (const auto &value : output.values)
      replay.published[rows[value.index].key] = value.value;
  };
  record(session.feed(before.data(), before.size(), 0));
  for (uint32_t now = 0; now < 5000; now += 5) {
    std::array<uint8_t, 6> request;
    if (!session.next_request(now, request))
      continue;
    replay.requests.push_back(request);
    if (echo)
      for (uint8_t byte : request)
        record(session.feed(&byte, 1, now));
    const uint16_t address = static_cast<uint16_t>(request[3] << 8 | request[4]);
    auto reply = replies.find(address);
    REQUIRE_MESSAGE(reply != replies.end(), "the Session asked for an Address the trace has no Reply for");
    now += 20;
    for (uint8_t byte : reply->second.bytes)
      record(session.feed(&byte, 1, now));
  }
  replay.counters = session.counters();
  return replay;
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

TEST_CASE("node trace: the Session asks for every Address the trace covers once, with a request build_read_request() makes") {
  const Replay replay = replay_trace(register_map::all_rows());

  const std::set<uint16_t> traced = traced_addresses();
  REQUIRE(traced.size() == 17);

  std::set<uint16_t> asked;
  for (const auto &request : replay.requests) {
    const uint16_t address = static_cast<uint16_t>(request[3] << 8 | request[4]);
    CHECK(asked.insert(address).second);
    auto expected = build_read_request(address);
    CHECK(request == expected);
  }
  CHECK(asked == traced);
  // Every Reply was answered, once, in the order the Session asked.
  CHECK(replay.answered.size() == 17);
}

TEST_CASE("node trace: replaying it counts no bus errors, with or without the Node's Read requests echoed back") {
  for (bool echo : {false, true}) {
    CAPTURE(echo);
    const Replay replay = replay_trace(register_map::all_rows(), {}, echo);
    CHECK(replay.answered.size() == 17);
    for (const CounterField &field : COUNTER_FIELDS) {
      CAPTURE(field.label);
      CHECK(replay.counters.*field.count == 0);
    }
  }
}

TEST_CASE("node trace: after a false start, every later Reply is answered once and at most one Address misses its cycle") {
  // 02 06 21 is a false start whose Length byte promises a 37-byte Frame. Without a reset the
  // Frame codec held every later Reply until 37 bytes had arrived, and the first two Addresses
  // were answered late, twice each.
  const Replay replay = replay_trace(register_map::all_rows(), {0x02, 0x06, 0x21});

  const std::set<uint16_t> traced = traced_addresses();
  REQUIRE(traced.size() == 17);

  const std::set<uint16_t> answered(replay.answered.begin(), replay.answered.end());
  CHECK(replay.answered.size() == answered.size());
  CHECK(answered.size() >= traced.size() - 1);
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
  const Replay replay = replay_trace(rows);
  const auto &decoded = replay.published;
  std::set<uint16_t> replied_addresses(replay.answered.begin(), replay.answered.end());

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
