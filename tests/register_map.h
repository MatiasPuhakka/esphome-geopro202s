#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include "value_decoder.h"

// The Register map's rows as codegen registers them, exported from register_map.py.
namespace register_map {

struct Row {
  std::string key;
  esphome::geopro_202s::Registration registration;
};

// The rows with these keys, in the order given. Fails the test if a key isn't in the Register map.
std::vector<Row> rows_named(const std::vector<std::string> &keys);

// Every row that reads `address`, in register_map.py's order.
std::vector<Row> rows_at(uint16_t address);

// The registrations of `rows`, in the same order, for decode_values().
std::vector<esphome::geopro_202s::Registration> registrations(const std::vector<Row> &rows);

}  // namespace register_map
