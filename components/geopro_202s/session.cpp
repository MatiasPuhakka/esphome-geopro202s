#include "session.h"

namespace esphome {
namespace geopro_202s {

Counters Counters::since(const Counters &earlier) const {
  Counters counts;
  counts.checksum_failures = this->checksum_failures - earlier.checksum_failures;
  counts.discarded_bytes = this->discarded_bytes - earlier.discarded_bytes;
  counts.retries = this->retries - earlier.retries;
  counts.give_ups = this->give_ups - earlier.give_ups;
  counts.undecoded_replies = this->undecoded_replies - earlier.undecoded_replies;
  return counts;
}

bool Counters::any() const {
  return this->checksum_failures != 0 || this->discarded_bytes != 0 || this->retries != 0 || this->give_ups != 0 ||
         this->undecoded_replies != 0;
}

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
    const std::vector<DecodedValue> values = decode_values(frame.address, frame.data, this->registrations_);
    if (values.empty())
      this->counters_.undecoded_replies++;
    output.values.insert(output.values.end(), values.begin(), values.end());
  }
  return output;
}

bool Session::next_request(uint32_t now, std::array<uint8_t, 6> &request) {
  uint16_t address;
  std::vector<RequestEvent> events;
  const bool send = this->scheduler_.next_request(now, address, events);
  for (const RequestEvent &event : events) {
    if (event.kind == RequestEvent::Kind::RETRY)
      this->counters_.retries++;
    else
      this->counters_.give_ups++;
  }
  if (!send)
    return false;
  request = build_read_request(address);
  return true;
}

Counters Session::counters() const {
  Counters counters = this->counters_;
  counters.checksum_failures = this->decoder_.checksum_failures();
  counters.discarded_bytes = this->decoder_.discarded_bytes();
  return counters;
}

bool BusErrorReport::take(uint32_t now, const Counters &counters, Counters &errors) {
  if (now - this->checked_at_ < this->interval_ms_)
    return false;
  const Counters since = counters.since(this->checked_);
  this->checked_at_ = now;
  this->checked_ = counters;
  if (!since.any())
    return false;
  errors = since;
  return true;
}

}  // namespace geopro_202s
}  // namespace esphome
