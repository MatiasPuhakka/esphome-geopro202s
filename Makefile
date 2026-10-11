CXXFLAGS ?= -std=c++17 -Wall -Wextra -O1

COMPONENT_DIR := components/geopro_202s
BUILD_DIR := build
ESPHOME ?= esphome
CONFIG_TEST := tests/all-keys.yaml
CONFIG_ARDUINO := tests/all-keys-arduino.yaml
NODE_CONFIG := geopro.yaml
TRACE_CONFIG := geopro-trace.yaml

# Component sources with no ESPHome dependency, built and tested on the host.
PURE_MODULES := frame poll_scheduler value_decoder
PURE_SRCS := $(addprefix $(COMPONENT_DIR)/,$(addsuffix .cpp,$(PURE_MODULES)))
TEST_SRCS := $(wildcard tests/*.cpp)
TEST_BIN := $(BUILD_DIR)/tests
# A raw trace from the Node that tests/trace_test.cpp replays; the test gets its absolute path.
NODE_TRACE := tests/traces/node-2026-10-09.log
# The Register map's rows for the host tests, rewritten whenever register_map.py changes.
# The export runs on plain python3 without ESPHome.
PYTHON ?= python3
REGISTER_MAP_ROWS := $(BUILD_DIR)/register_map_rows.inc

.PHONY: test pure-check tools-test check-secrets check-config check-node-config check-trace-config compile clean

test: pure-check $(TEST_BIN)
	./$(TEST_BIN)
	python3 -m unittest discover -s tests -p '*_test.py'

# The pure sources also run on the device, whose Arduino ESP32 build is C++11.
# Host tests use C++17, so check the pure sources on their own.
pure-check:
	@! grep -l '#include "esphome/' $(PURE_SRCS) $(PURE_SRCS:.cpp=.h)
	$(CXX) -std=c++11 -pedantic -Wall -Wextra -fsyntax-only -I$(COMPONENT_DIR) $(PURE_SRCS)

$(REGISTER_MAP_ROWS): $(COMPONENT_DIR)/register_map.py tests/export_register_map.py
	@mkdir -p $(BUILD_DIR)
	$(PYTHON) tests/export_register_map.py $< $@

$(TEST_BIN): $(TEST_SRCS) $(PURE_SRCS) $(wildcard $(COMPONENT_DIR)/*.h) $(wildcard tests/*.h) $(REGISTER_MAP_ROWS)
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -DNODE_TRACE='"$(CURDIR)/$(NODE_TRACE)"' -I$(COMPONENT_DIR) -Itests -I$(BUILD_DIR) -o $@ $(TEST_SRCS) $(PURE_SRCS)

# Runs the Python tools' tests offline against recorded Home Assistant JSON, with the stdlib only.
tools-test:
	python3 -I -m unittest discover -t . -s tools/tests

# Credentials live in the gitignored secrets.yaml and reach configs through !secret.
# Prints file:line only, so a leaked value stays out of the CI log.
check-secrets:
	@if git grep -nE '^[[:space:]]*(key|password):[[:space:]]*[^![:space:]]' -- '*.yaml' ':!.github' | cut -d: -f1,2 | grep .; then \
		echo "These lines hold a key or password inline. Move the value to secrets.yaml and use !secret."; \
		exit 1; \
	fi

# Validates a config that loads the component from this checkout and sets every key.
# ESPHome prints config errors on stdout, so the config checks keep it in $(BUILD_DIR)
# and print it on failure. Secrets appear there only as their !secret names.
check-config:
	@mkdir -p $(BUILD_DIR)
	$(ESPHOME) config $(CONFIG_TEST) > $(BUILD_DIR)/config.out || { cat $(BUILD_DIR)/config.out; exit 1; }

# Validates the Node's config and fails on deprecation warnings, so an option ESPHome is
# about to remove fails here before it breaks a build. Needs secrets.yaml next to
# geopro.yaml (CI writes a dummy one) and ESPHome 2026.9.1 or newer.
check-node-config:
	@mkdir -p $(BUILD_DIR)
	$(ESPHOME) config $(NODE_CONFIG) > $(BUILD_DIR)/node-config.out 2> $(BUILD_DIR)/node-config.log || { cat $(BUILD_DIR)/node-config.out $(BUILD_DIR)/node-config.log; exit 1; }
	@if grep -qi deprecat $(BUILD_DIR)/node-config.log; then cat $(BUILD_DIR)/node-config.log; exit 1; fi

# Validates the trace-capture overlay, which includes geopro.yaml. Same needs as
# check-node-config.
check-trace-config:
	@mkdir -p $(BUILD_DIR)
	$(ESPHOME) config $(TRACE_CONFIG) > $(BUILD_DIR)/trace-config.out 2> $(BUILD_DIR)/trace-config.log || { cat $(BUILD_DIR)/trace-config.out $(BUILD_DIR)/trace-config.log; exit 1; }
	@if grep -qi deprecat $(BUILD_DIR)/trace-config.log; then cat $(BUILD_DIR)/trace-config.log; exit 1; fi

# Builds firmware for both ESP32 frameworks. Slow on the first run (toolchain download).
compile:
	$(ESPHOME) compile $(CONFIG_TEST)
	$(ESPHOME) compile $(CONFIG_ARDUINO)

clean:
	rm -rf $(BUILD_DIR)
