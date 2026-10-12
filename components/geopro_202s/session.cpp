#include "session.h"

namespace esphome {
namespace geopro_202s {

EntryId Session::add_value(PollGroup group, const Registration &registration) {
  this->scheduler_.add_address(group, registration.address);
  this->registrations_.push_back(registration);
  return this->registrations_.size() - 1;
}

SessionOutput Session::feed(const uint8_t *bytes, size_t len, uint32_t now) {
  SessionOutput output;
  for (const Frame &frame : this->decoder_.feed(bytes, len)) {
    // A frame without data is a read request (an echo of our own, say), not a reply.
    if (frame.data.empty())
      continue;
    this->scheduler_.on_frame(frame.address, now);
    output.answered.push_back(frame.address);
    for (const DecodedValue &value : decode_values(frame.address, frame.data, this->registrations_))
      output.values.push_back(value);
  }
  return output;
}

bool Session::next_request(uint32_t now, std::array<uint8_t, 6> &request) {
  uint16_t address;
  if (!this->scheduler_.next_request(now, address))
    return false;
  request = build_read_request(address);
  return true;
}

}  // namespace geopro_202s
}  // namespace esphome
