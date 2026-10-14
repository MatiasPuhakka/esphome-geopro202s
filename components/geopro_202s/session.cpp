#include "session.h"

namespace esphome {
namespace geopro_202s {

Counters Counters::since(const Counters &earlier) const {
  Counters counts;
  for (const CounterField &field : COUNTER_FIELDS)
    counts.*field.count = this->*field.count - earlier.*field.count;
  return counts;
}

bool Counters::any() const {
  for (const CounterField &field : COUNTER_FIELDS)
    if (this->*field.count != 0)
      return true;
  return false;
}

std::string Counters::describe() const {
  std::string line;
  for (const CounterField &field : COUNTER_FIELDS) {
    if (!line.empty())
      line += ", ";
    line += field.label;
    line += ' ';
    line += std::to_string(this->*field.count);
  }
  return line;
}

EntryId Session::add_value(PollGroup group, const Registration &registration) {
  this->scheduler_.add_address(group, registration.address);
  this->registrations_.push_back(registration);
  if (this->find_misses_(registration.address) == nullptr)
    this->misses_.push_back(Misses{registration.address, 0});
  return this->registrations_.size() - 1;
}

Session::Misses *Session::find_misses_(uint16_t address) {
  for (Misses &misses : this->misses_)
    if (misses.address == address)
      return &misses;
  return nullptr;
}

// The scheduler only asks for registered Addresses, so the given-up one has a miss count.
void Session::on_give_up_(uint16_t address, SessionOutput &output) {
  output.missed.push_back(address);
  Misses *misses = this->find_misses_(address);
  if (misses == nullptr || misses->count == STALE_AFTER_MISSED_CYCLES)
    return;  // already stale, and reported when it became so
  misses->count++;
  if (misses->count < STALE_AFTER_MISSED_CYCLES)
    return;
  for (size_t id = 0; id < this->registrations_.size(); id++)
    if (this->registrations_[id].address == address)
      output.stale.push_back(id);
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
    Misses *misses = this->find_misses_(frame.address);
    if (misses != nullptr)
      misses->count = 0;
    const std::vector<DecodedValue> values = decode_values(frame.address, frame.data, this->registrations_);
    if (values.empty())
      this->counters_.undecoded_replies++;
    output.values.insert(output.values.end(), values.begin(), values.end());
  }
  return output;
}

bool Session::next_request(uint32_t now, std::array<uint8_t, 6> &request, SessionOutput &output) {
  uint16_t address;
  std::vector<RequestEvent> events;
  const bool send = this->scheduler_.next_request(now, address, events);
  for (const RequestEvent &event : events) {
    if (event.kind == RequestEvent::Kind::RETRY) {
      this->counters_.retries++;
    } else {
      this->counters_.give_ups++;
      this->on_give_up_(event.address, output);
    }
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

bool BusErrorReport::take(uint32_t now, uint32_t interval_ms, const Counters &counters, Counters &errors,
                          uint32_t &span_ms) {
  if (now - this->checked_at_ < interval_ms)
    return false;
  const Counters since = counters.since(this->checked_);
  this->checked_at_ = now;
  this->checked_ = counters;
  if (!since.any())
    return false;
  errors = since;
  span_ms = now - this->logged_at_;
  this->logged_at_ = now;
  return true;
}

}  // namespace geopro_202s
}  // namespace esphome
