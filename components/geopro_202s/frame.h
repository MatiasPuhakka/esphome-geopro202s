#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <vector>

namespace esphome {
namespace geopro_202s {

// Wire format: 02 <command> <length> <address hi> <address lo> <data...> <checksum>
// where length counts the address and data bytes. The command byte is 0x81 in a
// read request and 0x06 in a reply; the decoder accepts any value there.
static const uint8_t FRAME_START = 0x02;
static const uint8_t FRAME_CMD_READ = 0x81;
static const uint8_t FRAME_MIN_LENGTH = 0x02;
static const uint8_t FRAME_MAX_LENGTH = 0x21;
static const size_t FRAME_OVERHEAD = 4;

struct Frame {
  uint8_t command;
  uint16_t address;
  std::vector<uint8_t> data;
};

// Low byte of the sum of the given bytes.
uint8_t frame_checksum(const uint8_t *bytes, size_t len);

std::array<uint8_t, 6> build_read_request(uint16_t address);

class FrameDecoder {
 public:
  // Returns the complete, checksum-verified frames the new bytes finish.
  std::vector<Frame> feed(const uint8_t *bytes, size_t len);

 protected:
  void drain_(std::vector<Frame> &out);

  std::vector<uint8_t> buffer_;
};

}  // namespace geopro_202s
}  // namespace esphome
