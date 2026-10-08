#include "doctest.h"

#include "poll_scheduler.h"

#include <cstdint>
#include <optional>
#include <vector>

using esphome::geopro_202s::PollScheduler;
using esphome::geopro_202s::REPLY_TIMEOUT_MS;
using esphome::geopro_202s::REQUEST_GAP_MS;

namespace {

std::optional<uint16_t> next(PollScheduler &scheduler, uint32_t now) {
  uint16_t address;
  if (scheduler.next_request(now, address))
    return address;
  return std::nullopt;
}

// Drives a scheduler the way the hub's loop does, with a fake millisecond clock
// that advances one tick per loop pass.
struct Harness {
  explicit Harness(uint32_t start = 0) : now(start) {}

  PollScheduler scheduler;
  uint32_t now;

  std::optional<uint16_t> poll() { return next(this->scheduler, this->now); }

  void advance(uint32_t ms) { this->now += ms; }

  void reply(uint16_t address) { this->scheduler.on_frame(address, this->now); }

  // Runs the loop for `ms` milliseconds with the controller answering every
  // request at once, and returns the addresses requested.
  std::vector<uint16_t> run_answering(uint32_t ms) {
    std::vector<uint16_t> sent;
    for (uint32_t i = 0; i < ms; i++) {
      if (auto address = this->poll()) {
        sent.push_back(*address);
        this->reply(*address);
      }
      this->advance(1);
    }
    return sent;
  }

  // Runs the loop for `ms` milliseconds with a silent controller.
  std::vector<uint16_t> run_silent(uint32_t ms) {
    std::vector<uint16_t> sent;
    for (uint32_t i = 0; i < ms; i++) {
      if (auto address = this->poll())
        sent.push_back(*address);
      this->advance(1);
    }
    return sent;
  }
};

using Addresses = std::vector<uint16_t>;

}  // namespace

TEST_CASE("values and banks are read at startup") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_value_address(0x2D);
  h.scheduler.add_bank_address(0x0C);
  h.scheduler.add_bank_address(0x0B);

  CHECK(h.run_answering(1000) == Addresses{0x01, 0x2D, 0x0C, 0x0B});
}

TEST_CASE("values every 10 s and banks every 60 s after startup") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_bank_address(0x0C);

  CHECK(h.run_answering(1000) == Addresses{0x01, 0x0C});

  // Until 10 s after the startup cycle nothing more is read.
  CHECK(h.run_answering(9000).empty());
  CHECK(h.run_answering(1) == Addresses{0x01});

  // Values are read on every 10 s mark; banks wait for 60 s.
  CHECK(h.run_answering(39999) == Addresses{0x01, 0x01, 0x01});
  CHECK(h.now == 50000);
  CHECK(h.run_answering(10000) == Addresses{0x01});
  CHECK(h.now == 60000);
  CHECK(h.run_answering(1000) == Addresses{0x01, 0x0C});
}

TEST_CASE("intervals come from the constructor and setters") {
  PollScheduler scheduler(1000, 5000);
  scheduler.add_value_address(0x01);
  scheduler.add_bank_address(0x0C);

  CHECK(next(scheduler, 0) == 0x01);
  scheduler.on_frame(0x01, 0);
  CHECK(next(scheduler, REQUEST_GAP_MS) == 0x0C);
  scheduler.on_frame(0x0C, REQUEST_GAP_MS);
  CHECK(next(scheduler, 999) == std::nullopt);
  CHECK(next(scheduler, 1000) == 0x01);
  scheduler.on_frame(0x01, 1000);

  scheduler.set_bank_interval(2000);
  CHECK(next(scheduler, 1999) == std::nullopt);
  CHECK(next(scheduler, 2000) == 0x01);
  scheduler.on_frame(0x01, 2000);
  CHECK(next(scheduler, 2000 + REQUEST_GAP_MS) == 0x0C);
}

TEST_CASE("values every 3 s and banks every 7 s with non-default intervals") {
  Harness h;
  h.scheduler.set_value_interval(3000);
  h.scheduler.set_bank_interval(7000);
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_bank_address(0x0C);

  CHECK(h.run_answering(1000) == Addresses{0x01, 0x0C});
  CHECK(h.run_answering(2000).empty());
  CHECK(h.now == 3000);

  // Values come due at 3, 6, 9 and 12 s, banks at 7 and 14 s.
  CHECK(h.run_answering(1000) == Addresses{0x01});
  CHECK(h.run_answering(3000) == Addresses{0x01});
  CHECK(h.run_answering(1000) == Addresses{0x0C});
  CHECK(h.run_answering(2000) == Addresses{0x01});
  CHECK(h.run_answering(3000) == Addresses{0x01});
  CHECK(h.now == 13000);
  CHECK(h.run_answering(1000).empty());
  CHECK(h.run_answering(1000) == Addresses{0x0C});
}

TEST_CASE("no new request while one is in flight") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_value_address(0x02);

  CHECK(h.poll() == 0x01);
  CHECK(h.scheduler.in_flight());
  for (uint32_t t = 0; t < REPLY_TIMEOUT_MS - 1; t++) {
    h.advance(1);
    CHECK(h.poll() == std::nullopt);
  }
}

TEST_CASE("a reply for the in-flight address completes it") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_value_address(0x02);

  CHECK(h.poll() == 0x01);
  h.advance(100);
  h.reply(0x01);
  CHECK_FALSE(h.scheduler.in_flight());

  // Requests are paced: the next one waits for the gap after the reply.
  h.advance(REQUEST_GAP_MS - 1);
  CHECK(h.poll() == std::nullopt);
  h.advance(1);
  CHECK(h.poll() == 0x02);
}

TEST_CASE("a reply for any other address does not complete the request") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_value_address(0x02);

  CHECK(h.poll() == 0x01);
  h.advance(10);
  h.reply(0x02);
  h.reply(0x0C);
  CHECK(h.scheduler.in_flight());
  h.advance(REQUEST_GAP_MS);
  CHECK(h.poll() == std::nullopt);
}

TEST_CASE("a frame with nothing in flight is ignored") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.reply(0x01);
  CHECK(h.poll() == 0x01);
}

TEST_CASE("a timeout triggers one retry and then moves on") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_value_address(0x02);

  CHECK(h.poll() == 0x01);
  h.advance(REPLY_TIMEOUT_MS - 1);
  CHECK(h.poll() == std::nullopt);

  h.advance(1);
  CHECK(h.poll() == 0x01);  // the retry
  h.advance(REPLY_TIMEOUT_MS - 1);
  CHECK(h.poll() == std::nullopt);

  h.advance(1);
  CHECK(h.poll() == std::nullopt);  // gives up and waits out the gap
  CHECK_FALSE(h.scheduler.in_flight());
  h.advance(REQUEST_GAP_MS);
  CHECK(h.poll() == 0x02);
}

TEST_CASE("a reply to the retry completes the request") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_value_address(0x02);

  CHECK(h.poll() == 0x01);
  h.advance(REPLY_TIMEOUT_MS);
  CHECK(h.poll() == 0x01);
  h.advance(100);
  h.reply(0x01);
  h.advance(REQUEST_GAP_MS);
  CHECK(h.poll() == 0x02);
}

TEST_CASE("a silent controller gets two attempts per address per cycle") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_bank_address(0x0C);

  CHECK(h.run_silent(5000) == Addresses{0x01, 0x01, 0x0C, 0x0C});
}

TEST_CASE("each address is requested once per cycle") {
  Harness h;
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_bank_address(0x0C);
  h.scheduler.add_bank_address(0x0C);

  CHECK(h.run_answering(1000) == Addresses{0x01, 0x0C});
}

TEST_CASE("an address still waiting from the last cycle is not queued twice") {
  // 30 addresses against a silent controller take 30 s per cycle, longer than
  // the 10 s value interval.
  Harness h;
  for (uint16_t address = 1; address <= 30; address++)
    h.scheduler.add_value_address(address);

  auto sent = h.run_silent(60000);
  // Every address is attempted twice in order. The cycles that came due in the
  // meantime skipped the addresses still waiting, so the next pass starts over
  // from the first address instead of repeating the backlog.
  REQUIRE(sent.size() >= 98);
  for (size_t i = 0; i < 60; i++)
    CHECK(sent[i] == 1 + i / 2);
  for (size_t i = 60; i < 98; i++)
    CHECK(sent[i] == 1 + (i - 60) / 2);
}

TEST_CASE("an address in both lists is requested once") {
  Harness h;
  h.scheduler.add_value_address(0x0C);
  h.scheduler.add_bank_address(0x0C);

  CHECK(h.run_answering(1000) == Addresses{0x0C});
}

TEST_CASE("no addresses means no requests") {
  Harness h;
  CHECK(h.run_answering(100000).empty());
}

TEST_CASE("the millisecond counter wrapping around") {
  // Start just before the 32-bit counter wraps.
  Harness h(UINT32_MAX - 4999);
  h.scheduler.add_value_address(0x01);
  h.scheduler.add_bank_address(0x0C);

  CHECK(h.run_answering(1000) == Addresses{0x01, 0x0C});

  // The value cycle comes due 10 s after startup, 5 s after the wrap.
  CHECK(h.run_answering(9000).empty());
  CHECK(h.run_answering(1) == Addresses{0x01});
  CHECK(h.now == 5001);

  // The timeout still fires across the wrap.
  Harness t(UINT32_MAX - 100);
  t.scheduler.add_value_address(0x01);
  t.scheduler.add_value_address(0x02);
  CHECK(t.poll() == 0x01);
  t.advance(REPLY_TIMEOUT_MS - 1);
  CHECK(t.poll() == std::nullopt);
  t.advance(1);
  CHECK(t.poll() == 0x01);
}
