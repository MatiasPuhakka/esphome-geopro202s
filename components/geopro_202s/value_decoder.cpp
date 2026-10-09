#include "value_decoder.h"

namespace esphome {
namespace geopro_202s {

static size_t expected_data_length(const Registration &registration) {
  if (registration.group == PollGroup::BANK)
    return BANK_DATA_LENGTH;
  return static_cast<size_t>(registration.offset) + registration.rule.width;
}

static bool decode_one(const std::vector<uint8_t> &data, const Registration &registration, float &value) {
  const DecodeRule &rule = registration.rule;
  const uint8_t offset = registration.offset;
  if (rule.width != 1 && rule.width != 2)
    return false;
  if (rule.mask == 0 && rule.divisor == 0)
    return false;
  if (data.size() != expected_data_length(registration))
    return false;
  if (static_cast<size_t>(offset) + rule.width > data.size())
    return false;

  uint32_t raw = 0;
  for (uint8_t i = 0; i < rule.width; i++)
    raw = (raw << 8) | data[offset + i];

  if (rule.mask != 0) {
    value = (raw & rule.mask) != 0 ? 1.0f : 0.0f;
    return true;
  }

  int32_t number = static_cast<int32_t>(raw);
  const uint32_t sign_bit = 1u << (rule.width * 8 - 1);
  if (rule.is_signed && (raw & sign_bit))
    number -= static_cast<int32_t>(sign_bit << 1);
  value = static_cast<float>(number) / rule.divisor;
  return true;
}

std::vector<DecodedValue> decode_values(uint16_t address, const std::vector<uint8_t> &data,
                                        const std::vector<Registration> &registrations) {
  std::vector<DecodedValue> results;
  for (size_t i = 0; i < registrations.size(); i++) {
    const Registration &registration = registrations[i];
    if (registration.address != address)
      continue;
    float value;
    if (decode_one(data, registration, value))
      results.push_back(DecodedValue{i, value});
  }
  return results;
}

}  // namespace geopro_202s
}  // namespace esphome
