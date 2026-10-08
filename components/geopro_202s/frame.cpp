#include "frame.h"

#include <algorithm>
#include <utility>

namespace esphome {
namespace geopro_202s {

uint8_t frame_checksum(const uint8_t *bytes, size_t len) {
  uint8_t sum = 0;
  for (size_t i = 0; i < len; i++) {
    sum += bytes[i];
  }
  return sum;
}

std::array<uint8_t, 6> build_read_request(uint16_t address) {
  std::array<uint8_t, 6> frame = {FRAME_START, FRAME_CMD_READ, 0x02, static_cast<uint8_t>(address >> 8),
                                  static_cast<uint8_t>(address & 0xFF), 0x00};
  frame[5] = frame_checksum(frame.data() + 1, frame.size() - 2);
  return frame;
}

std::vector<Frame> FrameDecoder::feed(const uint8_t *bytes, size_t len) {
  std::vector<Frame> out;
  for (size_t i = 0; i < len; i++) {
    this->buffer_.push_back(bytes[i]);
    this->drain_(out);
  }
  return out;
}

void FrameDecoder::drain_(std::vector<Frame> &out) {
  auto &buf = this->buffer_;
  while (true) {
    auto start = std::find(buf.begin(), buf.end(), FRAME_START);
    buf.erase(buf.begin(), start);
    if (buf.size() < 3)
      return;

    uint8_t length = buf[2];
    if (length < FRAME_MIN_LENGTH || length > FRAME_MAX_LENGTH) {
      buf.erase(buf.begin());
      continue;
    }

    size_t frame_size = length + FRAME_OVERHEAD;
    if (buf.size() < frame_size)
      return;

    if (frame_checksum(buf.data() + 1, frame_size - 2) != buf[frame_size - 1]) {
      buf.erase(buf.begin());
      continue;
    }

    Frame frame;
    frame.command = buf[1];
    frame.address = (static_cast<uint16_t>(buf[3]) << 8) | buf[4];
    frame.data.assign(buf.begin() + 5, buf.begin() + frame_size - 1);
    out.push_back(std::move(frame));
    buf.erase(buf.begin(), buf.begin() + frame_size);
  }
}

}  // namespace geopro_202s
}  // namespace esphome
