#pragma once

#include "frame.h"
#include "poll_scheduler.h"
#include "value_decoder.h"

#include <array>
#include <cstddef>
#include <cstdint>
#include <vector>

namespace esphome {
namespace geopro_202s {

// Identifies one registered value. Ids count up from 0 in the order add_value() is called,
// so the hub can keep its entities in a vector indexed by id.
using EntryId = size_t;

// What the bytes passed to Session::feed() produced.
struct SessionOutput {
  // The Values to publish, each with the entry it belongs to.
  std::vector<DecodedValue> values;
  // The Address of each Reply received, in order, whether or not it decoded.
  std::vector<uint16_t> answered;
};

// The loop's decisions with no I/O: received bytes and the time go in, Read requests and
// decoded Values come out. It owns what counts as a Reply, when a request is done and
// which entry gets each Value. The hub moves bytes and Values between it and ESPHome.
// Like PollScheduler it has no clock: the caller passes millis() on every call.
class Session {
 public:
  void set_value_interval(uint32_t interval_ms) { this->scheduler_.set_value_interval(interval_ms); }
  void set_bank_interval(uint32_t interval_ms) { this->scheduler_.set_bank_interval(interval_ms); }

  // Registers a value and returns its id. The scheduler reads each Address once,
  // however many values share it.
  EntryId add_value(PollGroup group, const Registration &registration);

  const std::vector<Registration> &registrations() const { return this->registrations_; }

  SessionOutput feed(const uint8_t *bytes, size_t len, uint32_t now);

  // Returns true and sets `request` when a Read request should be sent now.
  bool next_request(uint32_t now, std::array<uint8_t, 6> &request);

 protected:
  FrameDecoder decoder_;
  PollScheduler scheduler_;
  std::vector<Registration> registrations_;
};

}  // namespace geopro_202s
}  // namespace esphome
