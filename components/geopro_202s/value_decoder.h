#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>

#include "poll_scheduler.h"

namespace esphome {
namespace geopro_202s {

// How to turn a value's bytes into a number: how many bytes it spans
// (big-endian), whether the top bit is a sign bit, what to divide the raw
// number by, and, for a Status bit, which bits of the word to test.
// Generated code calls the constructor rather than using designated
// initializers, which C++11 lacks.
struct DecodeRule {
  constexpr DecodeRule(uint8_t width, bool is_signed, uint16_t divisor = 1, uint16_t mask = 0)
      : width(width), is_signed(is_signed), divisor(divisor), mask(mask) {}

  uint8_t width;
  bool is_signed;
  // The decoded number is the raw number divided by this. Ignored when `mask` is set.
  uint16_t divisor;
  // When non-zero, the value is 1 if any of these bits is set in the raw
  // bytes and 0 otherwise.
  uint16_t mask;
};

// Data bytes in a Bank reply.
static const size_t BANK_DATA_LENGTH = 31;

// One configured value: the address whose reply carries it, where it starts in
// that reply's data, how to decode it, and which poll group reads it. Several
// registrations can share an address; one reply then feeds them all.
struct Registration {
  uint16_t address;
  uint8_t offset;
  DecodeRule rule;
  PollGroup group;
};

struct DecodedValue {
  // Position of the registration in the list passed to decode_values().
  size_t index;
  float value;
};

// Decodes every registration for `address` from that reply's data bytes.
// A registration produces no result when the reply's data length is not the
// one its group expects (BANK_DATA_LENGTH for a Bank, offset + width for a
// single value), when it is for another address, or when its rule has an
// unsupported width or a zero divisor.
std::vector<DecodedValue> decode_values(uint16_t address, const std::vector<uint8_t> &data,
                                        const std::vector<Registration> &registrations);

}  // namespace geopro_202s
}  // namespace esphome
