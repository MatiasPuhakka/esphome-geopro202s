CXXFLAGS ?= -std=c++17 -Wall -Wextra -O1

COMPONENT_DIR := components/geopro_202s
BUILD_DIR := build
ESPHOME ?= esphome
CONFIG_TEST := tests/all-keys.yaml

# Component sources that don't include ESPHome headers can be built on the host.
PURE_SRCS := $(shell grep -L '\#include "esphome/' $(COMPONENT_DIR)/*.cpp)
TEST_SRCS := $(wildcard tests/*.cpp)
TEST_BIN := $(BUILD_DIR)/tests

.PHONY: test check-config clean

test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(TEST_SRCS) $(PURE_SRCS) $(wildcard $(COMPONENT_DIR)/*.h) tests/doctest.h
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -I$(COMPONENT_DIR) -Itests -o $@ $(TEST_SRCS) $(PURE_SRCS)

# Validates a config that loads the component from this checkout and sets every key.
check-config:
	$(ESPHOME) config $(CONFIG_TEST) > /dev/null

clean:
	rm -rf $(BUILD_DIR)
