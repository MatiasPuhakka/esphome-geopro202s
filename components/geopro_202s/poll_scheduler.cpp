#include "poll_scheduler.h"

#include <algorithm>

namespace esphome {
namespace geopro_202s {

namespace {

void add_unique(std::vector<uint16_t> &addresses, uint16_t address) {
  if (std::find(addresses.begin(), addresses.end(), address) == addresses.end())
    addresses.push_back(address);
}

}  // namespace

void PollScheduler::add_value_address(uint16_t address) { add_unique(this->values_.addresses, address); }

void PollScheduler::add_bank_address(uint16_t address) { add_unique(this->banks_.addresses, address); }

bool PollScheduler::next_request(uint32_t now, uint16_t &address) {
  this->start_due_cycles_(now);

  if (this->in_flight_) {
    if (now - this->sent_at_ < REPLY_TIMEOUT_MS)
      return false;
    if (this->attempts_ <= REQUEST_RETRIES) {
      this->attempts_++;
      this->sent_at_ = now;
      address = this->in_flight_address_;
      return true;
    }
    this->finish_request_(now);
  }

  if (this->pending_.empty())
    return false;
  if (this->idle_since_set_ && now - this->idle_since_ < REQUEST_GAP_MS)
    return false;

  this->in_flight_ = true;
  this->in_flight_address_ = this->pending_.front();
  this->pending_.pop_front();
  this->sent_at_ = now;
  this->attempts_ = 1;
  address = this->in_flight_address_;
  return true;
}

void PollScheduler::on_frame(uint16_t address, uint32_t now) {
  if (this->in_flight_ && address == this->in_flight_address_)
    this->finish_request_(now);
}

void PollScheduler::start_due_cycles_(uint32_t now) {
  this->start_cycle_(this->values_, this->value_interval_ms_, now);
  this->start_cycle_(this->banks_, this->bank_interval_ms_, now);
}

void PollScheduler::start_cycle_(Group &group, uint32_t interval_ms, uint32_t now) {
  if (group.started && now - group.cycle_start < interval_ms)
    return;
  group.started = true;
  group.cycle_start = now;
  for (uint16_t address : group.addresses)
    this->enqueue_(address);
}

void PollScheduler::enqueue_(uint16_t address) {
  // An address still waiting from an earlier cycle keeps its place instead of
  // being queued twice.
  if (std::find(this->pending_.begin(), this->pending_.end(), address) != this->pending_.end())
    return;
  this->pending_.push_back(address);
}

void PollScheduler::finish_request_(uint32_t now) {
  this->in_flight_ = false;
  this->idle_since_set_ = true;
  this->idle_since_ = now;
}

}  // namespace geopro_202s
}  // namespace esphome
