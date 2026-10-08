#pragma once

#include <cstdint>
#include <deque>
#include <vector>

namespace esphome {
namespace geopro_202s {

// Default read intervals, in milliseconds.
static const uint32_t DEFAULT_VALUE_INTERVAL_MS = 10000;
static const uint32_t DEFAULT_BANK_INTERVAL_MS = 60000;

// How long to wait for a reply before giving up on a request. A 37-byte bank
// reply takes about 77 ms on the wire at 4800 baud and the 6-byte request about
// 13 ms more. The controller's own latency is unknown, so 500 ms leaves several
// times the transfer time as margin while still noticing a lost reply quickly.
static const uint32_t REPLY_TIMEOUT_MS = 500;

// A request that times out is sent once more, then dropped until its next cycle.
// One retry covers a single corrupted frame; a controller that stays silent
// shouldn't stall the other addresses.
static const uint8_t REQUEST_RETRIES = 1;

// Quiet time on the bus after a reply (or a dropped request) before the next
// request, so the controller isn't addressed back to back.
static const uint32_t REQUEST_GAP_MS = 50;

// Decides which address to read next. It has no clock of its own: the caller
// passes the current millis() value on every call, and differences between
// times are taken modulo 2^32, so the counter wrapping around is harmless.
class PollScheduler {
 public:
  PollScheduler(uint32_t value_interval_ms = DEFAULT_VALUE_INTERVAL_MS,
                uint32_t bank_interval_ms = DEFAULT_BANK_INTERVAL_MS)
      : value_interval_ms_(value_interval_ms), bank_interval_ms_(bank_interval_ms) {}

  // Adding the same address more than once has no effect.
  void add_value_address(uint16_t address);
  void add_bank_address(uint16_t address);
  void set_value_interval(uint32_t interval_ms) { this->value_interval_ms_ = interval_ms; }
  void set_bank_interval(uint32_t interval_ms) { this->bank_interval_ms_ = interval_ms; }

  // Returns true and sets `address` when a read request should be sent now.
  // The first call starts a cycle of every value and bank address.
  // (Not std::optional: ESPHome's Arduino ESP32 builds use C++11.)
  bool next_request(uint32_t now, uint16_t &address);

  // Report a received frame. Only a frame for the in-flight address completes it.
  void on_frame(uint16_t address, uint32_t now);

  bool in_flight() const { return this->in_flight_; }

 protected:
  struct Group {
    std::vector<uint16_t> addresses;
    bool started{false};
    uint32_t cycle_start{0};
  };

  void start_due_cycles_(uint32_t now);
  void start_cycle_(Group &group, uint32_t interval_ms, uint32_t now);
  void enqueue_(uint16_t address);
  void finish_request_(uint32_t now);

  uint32_t value_interval_ms_;
  uint32_t bank_interval_ms_;
  Group values_;
  Group banks_;

  std::deque<uint16_t> pending_;

  bool in_flight_{false};
  uint16_t in_flight_address_{0};
  uint32_t sent_at_{0};
  uint8_t attempts_{0};

  bool idle_since_set_{false};
  uint32_t idle_since_{0};
};

}  // namespace geopro_202s
}  // namespace esphome
