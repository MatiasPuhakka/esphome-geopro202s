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
#include <map>
#include <vector>

namespace esphome {
namespace geopro_202s {

static const char *const TAG = "geopro_202s";

// Status word bit masks
static const uint8_t BITMASK_DIGI1 = 0x01;
static const uint8_t BITMASK_DIGI2 = 0x02;
static const uint8_t BITMASK_DIGI3 = 0x04;
static const uint8_t BITMASK_EL_HEATER = 0x08;
static const uint8_t BITMASK_COMPRESSOR = 0x10;

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

  // Register sensors
  void register_temp_sensor(uint8_t id, sensor::Sensor *sensor) {
    this->temp_sensors_[id] = sensor;
  }

  void register_valve_sensor(uint8_t id, sensor::Sensor *sensor) {
    this->valve_sensors_[id] = sensor;
  }

  void register_hour_sensor(uint8_t id, sensor::Sensor *sensor) {
    this->hour_sensors_[id] = sensor;
  }

  void register_status_sensor(sensor::Sensor *sensor) {
    this->status_sensor_ = sensor;
  }

  // Register binary sensors for status bits
  void register_status_bit(uint16_t mask, binary_sensor::BinarySensor *sensor) {
    this->status_bits_[mask] = sensor;
  }

  // Register a value read from a configuration bank
  void register_bank_sensor(uint8_t bank_id, uint8_t offset, DecodeRule rule, sensor::Sensor *sensor) {
    this->bank_values_.push_back(Registration{bank_id, offset, rule});
    this->bank_sensors_.push_back(sensor);
  }

 protected:
  // Message handling
  void handle_frame_(const Frame &frame);
  void send_request_(uint16_t address);

  // Processing different response types
  void process_temperature_(uint8_t id, const uint8_t *data);
  void process_valve_(uint8_t id, const uint8_t *data);

  FrameDecoder decoder_;
  PollScheduler scheduler_;

  // Registered sensors
  std::map<uint8_t, sensor::Sensor *> temp_sensors_{};
  std::map<uint8_t, sensor::Sensor *> valve_sensors_{};
  std::map<uint8_t, sensor::Sensor *> hour_sensors_{};
  sensor::Sensor *status_sensor_{nullptr};
  std::map<uint16_t, binary_sensor::BinarySensor *> status_bits_{};
  // Bank values and their sensors, matched by index
  std::vector<Registration> bank_values_{};
  std::vector<sensor::Sensor *> bank_sensors_{};
};

} // namespace geopro_202s
} // namespace esphome