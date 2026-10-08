#include "value_decoder.h"

namespace esphome {
namespace geopro_202s {

static bool decode_one(const std::vector<uint8_t> &data, uint8_t offset, DecodeRule rule, float &value) {
  if (rule.width != 1 && rule.width != 2)
    return false;
  if (static_cast<size_t>(offset) + rule.width > data.size())
    return false;

  uint32_t raw = 0;
  for (uint8_t i = 0; i < rule.width; i++)
    raw = (raw << 8) | data[offset + i];

  if (!rule.is_signed) {
    value = static_cast<float>(raw);
    return true;
  }
  const uint32_t sign_bit = 1u << (rule.width * 8 - 1);
  int32_t signed_raw = static_cast<int32_t>(raw);
  if (raw & sign_bit)
    signed_raw -= static_cast<int32_t>(sign_bit << 1);
  value = static_cast<float>(signed_raw);
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
    if (decode_one(data, registration.offset, registration.rule, value))
      results.push_back(DecodedValue{i, value});
  }
  return results;
}

}  // namespace geopro_202s
}  // namespace esphome
