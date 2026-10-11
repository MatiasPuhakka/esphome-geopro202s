#include "register_map.h"

#include "doctest.h"

using esphome::geopro_202s::DecodeRule;
using esphome::geopro_202s::PollGroup;
using esphome::geopro_202s::Registration;

namespace register_map {

namespace {

// Every row, in register_map.py's order.
const std::vector<Row> &all_rows() {
  static const std::vector<Row> ROWS = {
#include "register_map_rows.inc"
  };
  return ROWS;
}

}  // namespace

std::vector<Row> rows_named(const std::vector<std::string> &keys) {
  std::vector<Row> found;
  for (const std::string &key : keys) {
    size_t before = found.size();
    for (const Row &row : all_rows())
      if (row.key == key)
        found.push_back(row);
    REQUIRE_MESSAGE(found.size() == before + 1, "no row for " << key << " in register_map.py");
  }
  return found;
}

std::vector<Row> rows_at(uint16_t address) {
  std::vector<Row> found;
  for (const Row &row : all_rows())
    if (row.registration.address == address)
      found.push_back(row);
  return found;
}

std::vector<Registration> registrations(const std::vector<Row> &rows) {
  std::vector<Registration> result;
  for (const Row &row : rows)
    result.push_back(row.registration);
  return result;
}

}  // namespace register_map
