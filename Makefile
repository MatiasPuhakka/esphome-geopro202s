CXXFLAGS ?= -std=c++17 -Wall -Wextra -O1

COMPONENT_DIR := components/geopro_202s
BUILD_DIR := build

# Component sources that don't include ESPHome headers can be built on the host.
PURE_SRCS := $(shell grep -L '\#include "esphome/' $(COMPONENT_DIR)/*.cpp)
TEST_SRCS := $(wildcard tests/*.cpp)
TEST_BIN := $(BUILD_DIR)/tests

.PHONY: test clean

test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(TEST_SRCS) $(PURE_SRCS) $(wildcard $(COMPONENT_DIR)/*.h) tests/doctest.h
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -I$(COMPONENT_DIR) -Itests -o $@ $(TEST_SRCS) $(PURE_SRCS)

clean:
	rm -rf $(BUILD_DIR)
