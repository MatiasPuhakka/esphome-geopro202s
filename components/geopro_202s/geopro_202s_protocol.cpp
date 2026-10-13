#include "geopro_202s_protocol.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace geopro_202s {

void Geopro202sComponent::add_value_(PollGroup group, const Registration &registration, const Target &target) {
  this->session_.add_value(group, registration);
  this->targets_.push_back(target);
}

void Geopro202sComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Geopro 202S...");
  if (this->component_revision_text_sensor_ != nullptr)
    this->component_revision_text_sensor_->publish_state(this->component_revision_);
}

void Geopro202sComponent::loop() {
  const uint32_t now = millis();

  uint8_t buffer[64];
  while (this->available()) {
    size_t len = 0;
    while (len < sizeof(buffer) && this->available())
      this->read_byte(&buffer[len++]);
    this->publish_(this->session_.feed(buffer, len, now));
  }

  std::array<uint8_t, 6> request;
  if (this->session_.next_request(now, request)) {
    ESP_LOGD(TAG, "Sending request for address 0x%04X", (unsigned) (request[3] << 8 | request[4]));
    this->write_array(request.data(), request.size());
  }

  this->report_bus_errors_(now);
}

// Logs the bus errors counted since the last check at WARN, which the Node's INFO logger
// keeps, and nothing when there are none. The bank cycle sets the cadence, not the value
// cycle: every Address is read at least once per bank interval, so one line covers a pass
// over the whole Register map, and a Controller that stops answering costs one line a
// minute at the default intervals instead of six.
void Geopro202sComponent::report_bus_errors_(uint32_t now) {
  Counters errors;
  if (!this->bus_error_report_.take(now, this->session_.counters(), errors))
    return;
  ESP_LOGW(TAG,
           "Bus errors in the last %u s: Checksum failures %u, discarded bytes %u, timeouts %u (retries %u, "
           "give-ups %u), Replies that decoded nothing %u",
           (unsigned) (this->bus_error_report_.interval() / 1000), (unsigned) errors.checksum_failures,
           (unsigned) errors.discarded_bytes, (unsigned) errors.timeouts(), (unsigned) errors.retries,
           (unsigned) errors.give_ups, (unsigned) errors.undecoded_replies);
}

void Geopro202sComponent::publish_(const SessionOutput &output) {
  for (uint16_t address : output.answered)
    ESP_LOGD(TAG, "Received reply: address=0x%04X", address);
  const auto &registrations = this->session_.registrations();
  for (const DecodedValue &result : output.values) {
    const Registration &value = registrations[result.index];
    ESP_LOGV(TAG, "Address 0x%04X offset %u: %.2f", value.address, value.offset, result.value);
    this->targets_[result.index](result.value);
  }
}

void Geopro202sComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "Geopro 202S:");
  ESP_LOGCONFIG(TAG, "  Component revision: %s", this->component_revision_);
  const auto &registrations = this->session_.registrations();
  ESP_LOGCONFIG(TAG, "  Registered values: %u", (unsigned) registrations.size());
  for (size_t i = 0; i < registrations.size(); i++) {
    const Registration &value = registrations[i];
    ESP_LOGCONFIG(TAG, "    %s 0x%04X, offset %u, %u byte(s), %s, divisor %u, mask 0x%04X",
                  value.address_kind == AddressKind::BANK ? "Bank" : "Address", value.address, value.offset,
                  value.rule.width, value.rule.is_signed ? "signed" : "unsigned", value.rule.divisor,
                  value.rule.mask);
  }
}

} // namespace geopro_202s
} // namespace esphome
