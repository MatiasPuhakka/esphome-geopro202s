#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/core/log.h"
#include "esphome/core/hal.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include <map>
#include <utility>

namespace esphome {
namespace geopro_202s {

static const char *const TAG = "geopro_202s";

// Protocol constants
static const uint8_t MSG_START = 0x02;
static const uint8_t CMD_READ = 0x81;
static const uint8_t CMD_LEN = 0x02;

// Message types in responses
static const uint8_t TYPE_VALVE = 0x03;
static const uint8_t TYPE_TEMP = 0x04;
static const uint8_t TYPE_BANK = 0x21;

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
  void register_status_bit(uint8_t mask, binary_sensor::BinarySensor *sensor) {
    this->status_bits_[mask] = sensor;
  }

  // Register bank sensors
  void register_bank_sensor(uint8_t bank_id, uint8_t offset, sensor::Sensor *sensor) {
    this->bank_sensors_[std::make_pair(bank_id, offset)] = sensor;
  }

  // Update schedule methods
  void schedule_temperature_readings();
  void schedule_valve_readings();
  void schedule_status_readings();
  void schedule_bank_readings();

 protected:
  // Message handling
  void handle_char_(uint8_t c);
  void process_message_();
  void send_request_(uint8_t id);
  uint8_t calculate_crc_(const uint8_t *data, uint8_t len);

  // Processing different response types
  void process_temperature_(uint8_t id, const uint8_t *data);
  void process_valve_(uint8_t id, const uint8_t *data);
  void process_bank_(uint8_t bank_id, const uint8_t *data);
  void update_bank_sensor(uint8_t bank_id, uint8_t offset, int8_t value);
  void update_bank_sensor(uint8_t bank_id, uint8_t offset, uint8_t value);

  // Message buffer
  std::vector<uint8_t> rx_buffer_;
  bool message_started_{false};
  uint32_t last_byte_time_{0};

  // Registered sensors
  std::map<uint8_t, sensor::Sensor *> temp_sensors_{};
  std::map<uint8_t, sensor::Sensor *> valve_sensors_{};
  std::map<uint8_t, sensor::Sensor *> hour_sensors_{};
  sensor::Sensor *status_sensor_{nullptr};
  std::map<uint8_t, binary_sensor::BinarySensor *> status_bits_{};
  std::map<std::pair<uint8_t, uint8_t>, sensor::Sensor *> bank_sensors_{};

  // Update scheduling
  uint32_t last_temp_reading_{0};
  uint32_t last_valve_reading_{0};
  uint32_t last_status_reading_{0};
  uint32_t last_bank_reading_{0};

  // Request queue for non-blocking communication
  std::vector<uint8_t> request_queue_{};
  uint32_t last_request_time_{0};
  static const uint32_t REQUEST_DELAY = 200;  // 200ms between requests
};

} // namespace geopro_202s
} // namespace esphome