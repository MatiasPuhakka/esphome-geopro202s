#include "geopro_202s_protocol.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
#include <set>

namespace esphome {
namespace geopro_202s {

static const uint32_t MIN_READ_INTERVAL = 10000;  // 10 seconds between readings
static const uint32_t BANK_READ_INTERVAL = 60000; // 60 seconds between bank readings
static const size_t BANK_DATA_LENGTH = 31;

void Geopro202sComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Geopro 202S...");
  // Initialize timestamps to trigger immediate readings
  this->last_bank_reading_ = 0;
  this->last_status_reading_ = 0;
}

void Geopro202sComponent::loop() {
  // Read available data first (process any incoming responses)
  while (this->available()) {
    uint8_t c;
    this->read_byte(&c);
    for (const auto &frame : this->decoder_.feed(&c, 1)) {
      this->handle_frame_(frame);
    }
  }

  const uint32_t now = millis();

  // Schedule regular updates - add requests to queue instead of sending immediately
  if (now - this->last_temp_reading_ > MIN_READ_INTERVAL) {
    this->schedule_temperature_readings();
    this->last_temp_reading_ = now;
  }

  if (now - this->last_valve_reading_ > MIN_READ_INTERVAL) {
    this->schedule_valve_readings();
    this->last_valve_reading_ = now;
  }

  if (now - this->last_status_reading_ > MIN_READ_INTERVAL) {
    this->schedule_status_readings();
    this->last_status_reading_ = now;
  }

  // Trigger bank readings immediately on first run or every 60 seconds
  if (this->last_bank_reading_ == 0 || (now - this->last_bank_reading_ > BANK_READ_INTERVAL)) {
    ESP_LOGD(TAG, "Triggering bank readings (last: %lu, now: %lu, interval: %u)", this->last_bank_reading_, now, BANK_READ_INTERVAL);
    this->schedule_bank_readings();
    this->last_bank_reading_ = now;
  }

  // Send one request from queue per loop (non-blocking)
  if (!this->request_queue_.empty() && (now - this->last_request_time_ >= REQUEST_DELAY)) {
    uint8_t id = this->request_queue_.front();
    this->request_queue_.erase(this->request_queue_.begin());
    this->send_request_(id);
    this->last_request_time_ = now;
  }
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
      this->process_bank_(id, data);
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

void Geopro202sComponent::send_request_(uint8_t id) {
  auto request = build_read_request(id);
  ESP_LOGD(TAG, "Sending request for sensor 0x%02X", id);
  this->write_array(request.data(), request.size());
}

void Geopro202sComponent::schedule_temperature_readings() {
  // Add temperature sensor requests to queue (non-blocking)
  for (const auto &sensor : this->temp_sensors_) {
    this->request_queue_.push_back(sensor.first);
  }
}

void Geopro202sComponent::schedule_valve_readings() {
  // Add valve sensor requests to queue
  for (const auto &sensor : this->valve_sensors_) {
    this->request_queue_.push_back(sensor.first);
  }
}

void Geopro202sComponent::schedule_status_readings() {
  // Add hour counter requests to queue
  for (const auto &sensor : this->hour_sensors_) {
    this->request_queue_.push_back(sensor.first);
  }

  // Schedule status word reading
  if (this->status_sensor_ != nullptr || !this->status_bits_.empty()) {
    uint8_t id = 0x2D;  // Status word ID
    this->request_queue_.push_back(id);
  }
}

void Geopro202sComponent::schedule_bank_readings() {
  // Get unique bank IDs from registered bank sensors
  std::set<uint8_t> banks_to_read;
  for (const auto &sensor : this->bank_sensors_) {
    banks_to_read.insert(sensor.first.first);  // bank_id is the first element of the pair
  }

  ESP_LOGD(TAG, "Scheduling bank readings: %d unique banks for %d bank sensors", banks_to_read.size(), this->bank_sensors_.size());

  // Add bank requests to queue
  for (uint8_t bank_id : banks_to_read) {
    ESP_LOGD(TAG, "Queuing bank request: 0x%02X", bank_id);
    this->request_queue_.push_back(bank_id);
  }
}

void Geopro202sComponent::process_bank_(uint8_t bank_id, const uint8_t *data) {
  // data holds the bank's 31 data bytes; offset 0 = data[0]

  // Bank 0x0C - Heating Circuit Settings
  if (bank_id == 0x0C) {
    ESP_LOGD(TAG, "Processing bank 0x0C");

    // L1 -20°C point (bytes[5], offset 0)
    update_bank_sensor(0x0C, 0, (int8_t)data[0]);
    // L1 0°C point (bytes[6], offset 1)
    update_bank_sensor(0x0C, 1, (int8_t)data[1]);
    // L1 +20°C point (bytes[7], offset 2)
    update_bank_sensor(0x0C, 2, (int8_t)data[2]);
    // L1 Min limit (bytes[8], offset 3)
    update_bank_sensor(0x0C, 3, (int8_t)data[3]);
    // L1 Max limit (bytes[9], offset 4)
    update_bank_sensor(0x0C, 4, (int8_t)data[4]);
    // L1 Night effect (bytes[10], offset 5)
    update_bank_sensor(0x0C, 5, (int8_t)data[5]);
    // L1 Autumn dry (bytes[19], offset 14)
    update_bank_sensor(0x0C, 14, (int8_t)data[14]);
    // L1 Outside temp delay (bytes[24], offset 19)
    update_bank_sensor(0x0C, 19, (int8_t)data[19]);
    // L1 Pre-increase (bytes[28], offset 23)
    update_bank_sensor(0x0C, 23, (int8_t)data[23]);
  }
  // Bank 0x2C - L1 Settings
  else if (bank_id == 0x2C) {
    ESP_LOGD(TAG, "Processing bank 0x2C");

    // L1 Summer close (bytes[13], offset 8)
    update_bank_sensor(0x2C, 8, (int8_t)data[8]);
  }
  // Bank 0x0B - Heat Pump Settings
  else if (bank_id == 0x0B) {
    ESP_LOGD(TAG, "Processing bank 0x0B");

    // Tank top winter (bytes[6], offset 1)
    update_bank_sensor(0x0B, 1, (int8_t)data[1]);
    // Tank top summer (bytes[7], offset 2)
    update_bank_sensor(0x0B, 2, (int8_t)data[2]);
    // Tank bottom diff (bytes[8], offset 3)
    update_bank_sensor(0x0B, 3, (int8_t)data[3]);
    // Tank top diff (bytes[9], offset 4)
    update_bank_sensor(0x0B, 4, (int8_t)data[4]);
    // Tank bottom min (bytes[10], offset 5)
    update_bank_sensor(0x0B, 5, (int8_t)data[5]);
    // EH delay (bytes[11], offset 6)
    update_bank_sensor(0x0B, 6, (int8_t)data[6]);
    // Tank top EH diff (bytes[12], offset 7)
    update_bank_sensor(0x0B, 7, (int8_t)data[7]);
    // Extra heating (bytes[13], offset 8)
    update_bank_sensor(0x0B, 8, (int8_t)data[8]);
    // Extra heating time (bytes[14], offset 9)
    update_bank_sensor(0x0B, 9, (int8_t)data[9]);
    // Control mode (bytes[15], offset 10)
    update_bank_sensor(0x0B, 10, (int8_t)data[10]);
    // Brine alert (bytes[16], offset 11)
    update_bank_sensor(0x0B, 11, (int8_t)data[11]);
    // DHW pre-open (bytes[17], offset 12)
    update_bank_sensor(0x0B, 12, (int8_t)data[12]);
    // DHW lock time (bytes[18], offset 13, uint8_t)
    update_bank_sensor(0x0B, 13, (uint8_t)data[13]);
    // Compressor lock time (bytes[19], offset 14)
    update_bank_sensor(0x0B, 14, (int8_t)data[14]);
  }
}

void Geopro202sComponent::update_bank_sensor(uint8_t bank_id, uint8_t offset, int8_t value) {
  auto it = this->bank_sensors_.find(std::make_pair(bank_id, offset));
  if (it != this->bank_sensors_.end()) {
    ESP_LOGD(TAG, "Bank 0x%02X offset %d: %d", bank_id, offset, value);
    it->second->publish_state(value);
  } else {
    ESP_LOGV(TAG, "Bank 0x%02X offset %d: %d (not registered)", bank_id, offset, value);
  }
}

void Geopro202sComponent::update_bank_sensor(uint8_t bank_id, uint8_t offset, uint8_t value) {
  auto it = this->bank_sensors_.find(std::make_pair(bank_id, offset));
  if (it != this->bank_sensors_.end()) {
    ESP_LOGD(TAG, "Bank 0x%02X offset %d: %d", bank_id, offset, value);
    it->second->publish_state(value);
  } else {
    ESP_LOGV(TAG, "Bank 0x%02X offset %d: %d (not registered)", bank_id, offset, value);
  }
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
    for (const auto &sensor : this->bank_sensors_) {
      ESP_LOGCONFIG(TAG, "    Bank 0x%02X, offset %d", sensor.first.first, sensor.first.second);
    }
  }
}

} // namespace geopro_202s
} // namespace esphome