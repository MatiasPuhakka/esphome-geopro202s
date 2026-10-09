#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/core/log.h"
#include "esphome/core/hal.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "frame.h"
#include "poll_scheduler.h"
#include "value_decoder.h"
#include <vector>

namespace esphome {
namespace geopro_202s {

static const char *const TAG = "geopro_202s";

class Geopro202sComponent : public Component, public uart::UARTDevice {
 public:
  Geopro202sComponent() = default;

  // Component interface methods
  void setup() override;
  void loop() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }

  // Poll intervals, in milliseconds. Leaving them unset keeps the scheduler's defaults.
  void set_value_interval(uint32_t interval_ms) { this->scheduler_.set_value_interval(interval_ms); }
  void set_bank_interval(uint32_t interval_ms) { this->scheduler_.set_bank_interval(interval_ms); }

  // Registers one value from the Register map: the address read for it (a
  // bank for settings), where it starts in the reply, and how to decode it.
  // A sensor publishes the decoded number, a binary sensor whether it is non-zero.
  void register_value(PollGroup group, uint16_t address, uint8_t offset, DecodeRule rule, sensor::Sensor *sensor) {
    this->add_value_(Registration{address, offset, rule, group}, Target{sensor, nullptr});
  }
  void register_value(PollGroup group, uint16_t address, uint8_t offset, DecodeRule rule,
                      binary_sensor::BinarySensor *binary_sensor) {
    this->add_value_(Registration{address, offset, rule, group}, Target{nullptr, binary_sensor});
  }

 protected:
  // Where a registration's decoded value is published. Exactly one is set.
  struct Target {
    sensor::Sensor *sensor;
    binary_sensor::BinarySensor *binary_sensor;
  };

  void add_value_(const Registration &registration, const Target &target);
  void handle_frame_(const Frame &frame);
  void send_request_(uint16_t address);

  FrameDecoder decoder_;
  PollScheduler scheduler_;

  // Registered values and where each one publishes, matched by index. They stay
  // apart because decode_values() is pure and reports results by registration index.
  std::vector<Registration> registrations_{};
  std::vector<Target> targets_{};
};

} // namespace geopro_202s
} // namespace esphome
