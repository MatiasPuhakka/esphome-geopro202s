#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/core/log.h"
#include "esphome/core/hal.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "session.h"
#include <array>
#include <functional>
#include <vector>

namespace esphome {
namespace geopro_202s {

static const char *const TAG = "geopro_202s";

// How each entity kind publishes a decoded value. The hub picks a platform here and
// nowhere else, as codegen does in _PLATFORMS in __init__.py.
inline void publish_value(sensor::Sensor *sensor, float value) { sensor->publish_state(value); }
inline void publish_value(binary_sensor::BinarySensor *binary_sensor, float value) {
  binary_sensor->publish_state(value != 0.0f);
}

class Geopro202sComponent : public Component, public uart::UARTDevice {
 public:
  Geopro202sComponent() = default;

  // Component interface methods
  void setup() override;
  void loop() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }

  // Poll intervals, in milliseconds. Codegen always sets both from the config (default 10 s and 60 s).
  void set_value_interval(uint32_t interval_ms) { this->session_.set_value_interval(interval_ms); }
  void set_bank_interval(uint32_t interval_ms) { this->session_.set_bank_interval(interval_ms); }

  // The Component's git revision, stamped by codegen: a short commit hash, "-dirty"
  // when built from uncommitted changes, or "unknown". The text sensor is optional.
  void set_component_revision(const char *revision) { this->component_revision_ = revision; }
  void set_component_revision_text_sensor(text_sensor::TextSensor *text_sensor) {
    this->component_revision_text_sensor_ = text_sensor;
  }

  // Registers one value from the Register map: which cycle reads its address,
  // whether that address is a bank or a single value, the address, where the
  // value starts in the reply, how to decode it, and the entity that publishes
  // it, of any kind publish_value() takes.
  template<typename Entity>
  void register_value(PollGroup group, AddressKind address_kind, uint16_t address, uint8_t offset, DecodeRule rule,
                      Entity *entity) {
    this->add_value_(group, Registration{address, offset, rule, address_kind},
                     [entity](float value) { publish_value(entity, value); });
  }

 protected:
  // Publishes a registration's decoded value on its entity.
  using Target = std::function<void(float)>;

  void add_value_(PollGroup group, const Registration &registration, const Target &target);
  void publish_(const SessionOutput &output);
  void report_bus_errors_(uint32_t now);

  const char *component_revision_{"unknown"};
  text_sensor::TextSensor *component_revision_text_sensor_{nullptr};

  Session session_;

  // Where each registered value publishes, indexed by the EntryId the Session gave it.
  std::vector<Target> targets_{};

  // When to log the Session's bus errors (see report_bus_errors_()).
  BusErrorReport bus_error_report_{};
};

} // namespace geopro_202s
} // namespace esphome
