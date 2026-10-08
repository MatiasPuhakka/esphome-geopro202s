#include "geopro_202s_protocol.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"

namespace esphome {
namespace geopro_202s {

void Geopro202sComponent::add_value_(PollGroup group, const Registration &registration, const Target &target) {
  this->registrations_.push_back(registration);
  this->groups_.push_back(group);
  this->targets_.push_back(target);
}

void Geopro202sComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Geopro 202S...");
  // The scheduler keeps each address once, however many values share it.
  for (size_t i = 0; i < this->registrations_.size(); i++)
    this->scheduler_.add_address(this->groups_[i], this->registrations_[i].address);
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
  if (frame.data.empty())
    return;

  auto results = decode_values(frame.address, frame.data, this->registrations_);
  if (results.empty()) {
    ESP_LOGV(TAG, "No value decoded from address 0x%04X", frame.address);
    return;
  }
  for (const auto &result : results) {
    const Registration &value = this->registrations_[result.index];
    const Target &target = this->targets_[result.index];
    ESP_LOGV(TAG, "Address 0x%04X offset %u: %.2f", value.address, value.offset, result.value);
    if (target.sensor != nullptr)
      target.sensor->publish_state(result.value);
    if (target.binary_sensor != nullptr)
      target.binary_sensor->publish_state(result.value != 0.0f);
  }
}

void Geopro202sComponent::send_request_(uint16_t address) {
  auto request = build_read_request(address);
  ESP_LOGD(TAG, "Sending request for address 0x%04X", address);
  this->write_array(request.data(), request.size());
}

void Geopro202sComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "Geopro 202S:");
  ESP_LOGCONFIG(TAG, "  Registered values: %u", (unsigned) this->registrations_.size());
  for (size_t i = 0; i < this->registrations_.size(); i++) {
    const Registration &value = this->registrations_[i];
    ESP_LOGCONFIG(TAG, "    %s 0x%04X, offset %u, %u byte(s), %s, divisor %u, mask 0x%04X",
                  this->groups_[i] == PollGroup::BANK ? "Bank" : "Address", value.address, value.offset,
                  value.rule.width, value.rule.is_signed ? "signed" : "unsigned", value.rule.divisor,
                  value.rule.mask);
  }
}

} // namespace geopro_202s
} // namespace esphome
