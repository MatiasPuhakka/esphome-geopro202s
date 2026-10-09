CXXFLAGS ?= -std=c++17 -Wall -Wextra -O1

COMPONENT_DIR := components/geopro_202s
BUILD_DIR := build
ESPHOME ?= esphome
CONFIG_TEST := tests/all-keys.yaml
CONFIG_ARDUINO := tests/all-keys-arduino.yaml

# Component sources with no ESPHome dependency, built and tested on the host.
PURE_MODULES := frame poll_scheduler value_decoder
PURE_SRCS := $(addprefix $(COMPONENT_DIR)/,$(addsuffix .cpp,$(PURE_MODULES)))
TEST_SRCS := $(wildcard tests/*.cpp)
TEST_BIN := $(BUILD_DIR)/tests

.PHONY: test pure-check check-config compile clean

test: pure-check $(TEST_BIN)
	./$(TEST_BIN)

# The pure sources also run on the device, whose Arduino ESP32 build is C++11.
# Host tests use C++17, so check the pure sources on their own.
pure-check:
	@! grep -l '#include "esphome/' $(PURE_SRCS) $(PURE_SRCS:.cpp=.h)
	$(CXX) -std=c++11 -pedantic -Wall -Wextra -fsyntax-only -I$(COMPONENT_DIR) $(PURE_SRCS)

$(TEST_BIN): $(TEST_SRCS) $(PURE_SRCS) $(wildcard $(COMPONENT_DIR)/*.h) tests/doctest.h
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -I$(COMPONENT_DIR) -Itests -o $@ $(TEST_SRCS) $(PURE_SRCS)

# Validates a config that loads the component from this checkout and sets every key.
check-config:
	$(ESPHOME) config $(CONFIG_TEST) > /dev/null

# Builds firmware for both ESP32 frameworks. Slow on the first run (toolchain download).
compile:
	$(ESPHOME) compile $(CONFIG_TEST)
	$(ESPHOME) compile $(CONFIG_ARDUINO)

clean:
	rm -rf $(BUILD_DIR)
