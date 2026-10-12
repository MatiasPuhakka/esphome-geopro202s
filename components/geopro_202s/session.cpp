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
  if (len == 0)
    return output;
  if (now - this->last_bytes_at_ > SILENCE_GAP_MS)
    this->decoder_.reset();
  this->last_bytes_at_ = now;
  for (const Frame &frame : this->decoder_.feed(bytes, len)) {
    // Only a Frame with Command byte 0x06 is a Reply. The Session ignores any other, such as
    // the Node's own Read request echoed back, whether or not it carries data.
    if (frame.command != FRAME_CMD_REPLY)
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
