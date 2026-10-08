#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

namespace esphome {
namespace geopro_202s {

// How to turn a value's bytes into a number: how many bytes it spans
// (big-endian) and whether the top bit is a sign bit.
// A plain aggregate, so codegen can brace-initialise it under C++11.
struct DecodeRule {
  uint8_t width;
  bool is_signed;
};

// One configured value: the address whose reply carries it, where it starts in
// that reply's data, and how to decode it.
struct Registration {
  uint16_t address;
  uint8_t offset;
  DecodeRule rule;
};

struct DecodedValue {
  // Position of the registration in the list passed to decode_values().
  size_t index;
  float value;
};

// Decodes every registration for `address` from that reply's data bytes.
// A registration whose bytes fall outside `data` produces no result, as does
// one for another address or with an unsupported width.
std::vector<DecodedValue> decode_values(uint16_t address, const std::vector<uint8_t> &data,
                                        const std::vector<Registration> &registrations);

}  // namespace geopro_202s
}  // namespace esphome
