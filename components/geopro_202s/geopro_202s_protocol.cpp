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

  // A give-up, and an Address going stale, come out of the request path: no bytes arrive to
  // feed. So the request path's output is published too, in the same loop.
  std::array<uint8_t, 6> request;
  SessionOutput output;
  const bool send = this->session_.next_request(now, request, output);
  this->publish_(output);
  if (send) {
    ESP_LOGD(TAG, "Sending request for address 0x%04X", (unsigned) (request[3] << 8 | request[4]));
    this->write_array(request.data(), request.size());
  }

  this->report_bus_errors_(now);
}

// Logs the bus errors counted since the last line at WARN, which the Node's INFO logger
// keeps, and nothing when there are none. The bank interval sets the cadence, not the value
// interval: it is the shortest span in which every Address gets read, and a Controller that
// stops answering costs one line a minute at the default intervals instead of six. The
// report keeps its own clock, so its spans aren't aligned with the bank cycle, but there is
// still at most one line per bank interval.
void Geopro202sComponent::report_bus_errors_(uint32_t now) {
  Counters errors;
  uint32_t span_ms;
  if (!this->bus_error_report_.take(now, this->session_.bank_interval(), this->session_.counters(), errors, span_ms))
    return;
  ESP_LOGW(TAG, "Bus errors in the last %u s: %s", (unsigned) (span_ms / 1000), errors.describe().c_str());
}

void Geopro202sComponent::publish_(const SessionOutput &output) {
  for (uint16_t address : output.answered)
    ESP_LOGD(TAG, "Received reply: address=0x%04X", address);
  const auto &registrations = this->session_.registrations();
  for (const DecodedValue &result : output.values) {
    const Registration &value = registrations[result.index];
    ESP_LOGV(TAG, "Address 0x%04X offset %u: %.2f", value.address, value.offset, result.value);
    this->targets_[result.index].publish(result.value);
  }
  for (uint16_t address : output.missed)
    ESP_LOGD(TAG, "No reply for address 0x%04X this cycle", address);
  // The entries at one Address go stale together, so one line per Address.
  uint16_t stale_address = 0;
  for (size_t i = 0; i < output.stale.size(); i++) {
    const EntryId entry = output.stale[i];
    const uint16_t address = registrations[entry].address;
    if (i == 0 || address != stale_address) {
      ESP_LOGW(TAG, "Address 0x%04X unanswered for %u cycles, its values are unknown until it replies", address,
               (unsigned) STALE_AFTER_MISSED_CYCLES);
      stale_address = address;
    }
    this->targets_[entry].invalidate();
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
