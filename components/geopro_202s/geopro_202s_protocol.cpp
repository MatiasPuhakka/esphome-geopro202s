#include "geopro_202s_protocol.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace geopro_202s {

static const uint16_t STATUS_WORD_ADDRESS = 0x2D;
static const size_t BANK_DATA_LENGTH = 31;

void Geopro202sComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Geopro 202S...");
  for (const auto &sensor : this->temp_sensors_)
    this->scheduler_.add_value_address(sensor.first);
  for (const auto &sensor : this->valve_sensors_)
    this->scheduler_.add_value_address(sensor.first);
  for (const auto &sensor : this->hour_sensors_)
    this->scheduler_.add_value_address(sensor.first);
  if (this->status_sensor_ != nullptr || !this->status_bits_.empty())
    this->scheduler_.add_value_address(STATUS_WORD_ADDRESS);
  for (const auto &value : this->bank_values_)
    this->scheduler_.add_bank_address(value.address);
}

void Geopro202sComponent::loop() {
  const uint32_t now = millis();

  while (this->available()) {
    uint8_t c;
    this->read_byte(&c);
    for (const auto &frame : this->decoder_.feed(&c, 1)) {
      // A frame without data is a read request (an echo of our own, say), not a reply.
      if (!frame.data.empty())
        this->scheduler_.on_frame(frame.address, now);
      this->handle_frame_(frame);
    }
  }

  uint16_t address;
  if (this->scheduler_.next_request(now, address))
    this->send_request_(address);
}

void Geopro202sComponent::handle_frame_(const Frame &frame) {
  ESP_LOGD(TAG, "Received frame: address=0x%04X, data length=%u", frame.address, (unsigned) frame.data.size());
  if (frame.address > 0xFF) {
    ESP_LOGV(TAG, "Unknown address: 0x%04X", frame.address);
    return;
  }

  uint8_t id = frame.address;
  const uint8_t *data = frame.data.data();
  switch (frame.data.size()) {
    case 1:
      this->process_valve_(id, data);
      break;

    case 2:
      this->process_temperature_(id, data);
      break;

    case BANK_DATA_LENGTH:
      for (const auto &result : decode_values(frame.address, frame.data, this->bank_values_)) {
        const Registration &value = this->bank_values_[result.index];
        ESP_LOGD(TAG, "Bank 0x%02X offset %u: %.0f", value.address, value.offset, result.value);
        this->bank_sensors_[result.index]->publish_state(result.value);
      }
      break;

    default:
      ESP_LOGV(TAG, "Unexpected data length %u for address 0x%02X", (unsigned) frame.data.size(), id);
      break;
  }
}

void Geopro202sComponent::process_temperature_(uint8_t id, const uint8_t *data) {
  // Handle temperature sensors (id <= 0x22)
  auto temp_it = this->temp_sensors_.find(id);
  if (temp_it != this->temp_sensors_.end()) {
    int16_t raw = (data[0] << 8) | data[1];
    float temp = raw / 100.0f;
    ESP_LOGD(TAG, "Temperature sensor 0x%02X: %.2f°C (raw: %d)", id, temp, raw);
    temp_it->second->publish_state(temp);
    return;
  }

  // Handle hour counters and status word (id >= 0x3A or 0x2D)
  auto hour_it = this->hour_sensors_.find(id);
  if (hour_it != this->hour_sensors_.end()) {
    uint16_t value = (data[0] << 8) | data[1];
    ESP_LOGV(TAG, "Hour sensor 0x%02X: %d", id, value);
    hour_it->second->publish_state(value);
    return;
  }

  // Handle status word: decode once for the word sensor and every bit sensor
  if (id == 0x2D && (this->status_sensor_ != nullptr || !this->status_bits_.empty())) {
    uint16_t value = (data[0] << 8) | data[1];
    ESP_LOGD(TAG, "Status word: 0x%04X", value);
    if (this->status_sensor_ != nullptr)
      this->status_sensor_->publish_state(value);

    // Update binary sensors based on status word bits
    for (auto &bit_sensor : this->status_bits_) {
      bool state = (value & bit_sensor.first) != 0;
      bit_sensor.second->publish_state(state);
    }
    return;
  }
}

void Geopro202sComponent::process_valve_(uint8_t id, const uint8_t *data) {
  auto it = this->valve_sensors_.find(id);
  if (it == this->valve_sensors_.end())
    return;

  uint8_t position = data[0];

  ESP_LOGV(TAG, "Valve 0x%02X position: %d%%", id, position);
  it->second->publish_state(position);
}

void Geopro202sComponent::send_request_(uint16_t address) {
  auto request = build_read_request(address);
  ESP_LOGD(TAG, "Sending request for address 0x%04X", address);
  this->write_array(request.data(), request.size());
}

void Geopro202sComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "Geopro 202S:");
  ESP_LOGCONFIG(TAG, "  Temperature sensors: %d", this->temp_sensors_.size());
  ESP_LOGCONFIG(TAG, "  Valve sensors: %d", this->valve_sensors_.size());
  ESP_LOGCONFIG(TAG, "  Hour sensors: %d", this->hour_sensors_.size());
  ESP_LOGCONFIG(TAG, "  Status bits: %d", this->status_bits_.size());
  ESP_LOGCONFIG(TAG, "  Bank sensors: %d", this->bank_sensors_.size());

  // Log registered bank sensors for debugging
  if (!this->bank_sensors_.empty()) {
    ESP_LOGCONFIG(TAG, "  Registered bank sensors:");
    for (const auto &value : this->bank_values_) {
      ESP_LOGCONFIG(TAG, "    Bank 0x%02X, offset %u, %u byte(s), %s", value.address, value.offset, value.rule.width,
                    value.rule.is_signed ? "signed" : "unsigned");
    }
  }
}

} // namespace geopro_202s
} // namespace esphome