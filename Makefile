CXXFLAGS ?= -std=c++17 -Wall -Wextra -O1

COMPONENT_DIR := components/geopro_202s
BUILD_DIR := build
# The ESPHome install every ESPHome target runs. ADR 0002 supports the 2026.9 series
# only, and the targets stop when $(ESPHOME) is another version. To use a 2026.9 install
# that isn't on PATH: make <target> ESPHOME=/path/to/esphome, or export ESPHOME.
ESPHOME ?= esphome
SUPPORTED_ESPHOME := 2026.9
# check-contract and update-contract import register_map.py, so they need the Python
# that has ESPHome installed: the python next to $(ESPHOME), as in a venv or CI's
# setup-python, else python3. PYTHON runs the host tests and doesn't need ESPHome.
ESPHOME_PYTHON ?= $(firstword $(wildcard $(dir $(shell command -v $(ESPHOME)))python) python3)
PYTHON ?= python3
CONFIG_TEST := tests/all-keys.yaml
CONFIG_ARDUINO := tests/all-keys-arduino.yaml
NODE_CONFIG := geopro.yaml
TRACE_CONFIG := geopro-trace.yaml

# Component sources with no ESPHome dependency, built and tested on the host.
PURE_MODULES := frame poll_scheduler value_decoder session
PURE_SRCS := $(addprefix $(COMPONENT_DIR)/,$(addsuffix .cpp,$(PURE_MODULES)))
TEST_SRCS := $(wildcard tests/*.cpp)
TEST_BIN := $(BUILD_DIR)/tests
# A raw trace from the Node that tests/trace_test.cpp replays; the test gets its absolute path.
NODE_TRACE := tests/traces/node-2026-10-09.log
# The Register map's rows for the host tests, rewritten whenever register_map.py changes.
# The export runs on plain python3 without ESPHome.
REGISTER_MAP_ROWS := $(BUILD_DIR)/register_map_rows.inc

.PHONY: test pure-check tools-test check-secrets dummy-secrets check-manual-links esphome-version check-config check-node-config check-trace-config check-contract update-contract compile compile-node clean

test: pure-check $(TEST_BIN)
	./$(TEST_BIN)
	$(PYTHON) -m unittest discover -s tests -p '*_test.py'

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

# Runs the tools' tests offline with the stdlib only: the Python tools against recorded Home
# Assistant JSON, and on macOS the PDF tools against the manual PDFs.
tools-test:
	python3 -I -m unittest discover -t . -s tools/tests

# Every link to a manual page anchor (manuals/*.md#s21) must resolve (ADR 0006).
check-manual-links:
	python3 -I tools/check_manual_links.py

# Credentials live in the gitignored secrets.yaml and reach configs through !secret.
# Prints file:line only, so a leaked value stays out of the CI log.
check-secrets:
	@if git grep -nE '^[[:space:]]*(key|password):[[:space:]]*[^![:space:]]' -- '*.yaml' ':!.github' | cut -d: -f1,2 | grep .; then \
		echo "These lines hold a key or password inline. Move the value to secrets.yaml and use !secret."; \
		exit 1; \
	fi

# Writes a secrets.yaml with a random API key, for CI and any checkout without the real
# one, so the config checks and compile-node run. It leaves an existing file alone. A
# dummy key can't flash the Node.
dummy-secrets:
	@if [ -e secrets.yaml ]; then \
		echo "secrets.yaml exists; leaving it alone."; \
	else \
		printf 'api_encryption_key: "%s"\n' "$$(head -c 32 /dev/urandom | base64)" > secrets.yaml; \
	fi

# Stops with a message unless $(ESPHOME) is a $(SUPPORTED_ESPHOME).x release. Every
# ESPHome target depends on it.
esphome-version:
	@version=$$($(ESPHOME) version 2>/dev/null | sed -n 's/^Version: //p'); \
	case "$$version" in \
		$(SUPPORTED_ESPHOME).*) ;; \
		*) echo "$(ESPHOME) is ESPHome $${version:-(not found)}, but this repo supports $(SUPPORTED_ESPHOME).x only (docs/adr/0002-supported-esphome-versions.md)."; \
		   echo "Point make at a $(SUPPORTED_ESPHOME).x install: make <target> ESPHOME=/path/to/esphome"; \
		   exit 1 ;; \
	esac

# Validates a config that loads the component from this checkout and sets every key.
# ESPHome prints config errors on stdout, so the config checks keep it in $(BUILD_DIR)
# and print it on failure. Secrets appear there only as their !secret names.
check-config: esphome-version
	@mkdir -p $(BUILD_DIR)
	$(ESPHOME) config $(CONFIG_TEST) > $(BUILD_DIR)/config.out || { cat $(BUILD_DIR)/config.out; exit 1; }

# Validates $(1) and fails on deprecation warnings, so an option ESPHome is about to
# remove fails here before it breaks a build. Writes ESPHome's output to $(2).out and
# its log to $(2).log in $(BUILD_DIR), and prints the log's warnings when it passes.
define check_with_warnings
	@mkdir -p $(BUILD_DIR)
	$(ESPHOME) config $(1) > $(BUILD_DIR)/$(2).out 2> $(BUILD_DIR)/$(2).log || { cat $(BUILD_DIR)/$(2).out $(BUILD_DIR)/$(2).log; exit 1; }
	@if grep -qi deprecat $(BUILD_DIR)/$(2).log; then cat $(BUILD_DIR)/$(2).log; exit 1; fi
	@grep -v '^INFO ' $(BUILD_DIR)/$(2).log || true
endef

# Validates the Node's config. Needs secrets.yaml next to geopro.yaml (dummy-secrets
# writes one).
check-node-config: esphome-version
	$(call check_with_warnings,$(NODE_CONFIG),node-config)

# Validates the trace-capture overlay, which includes geopro.yaml. Same needs as
# check-node-config.
check-trace-config: esphome-version
	$(call check_with_warnings,$(TRACE_CONFIG),trace-config)

# The Home Assistant entity contract, tests/entity-contract.txt: each key's platform and
# entity options, and the Node's entity names and IDs, taken from both config checks'
# output. check-contract fails with a diff when it changed; update-contract rewrites it.
check-contract: check-config check-node-config
	$(ESPHOME_PYTHON) tests/entity_contract.py check $(BUILD_DIR)/config.out $(BUILD_DIR)/node-config.out

update-contract: check-config check-node-config
	$(ESPHOME_PYTHON) tests/entity_contract.py update $(BUILD_DIR)/config.out $(BUILD_DIR)/node-config.out

# Builds firmware for both ESP32 frameworks. Slow on the first run (toolchain download).
compile: esphome-version
	$(ESPHOME) compile $(CONFIG_TEST)
	$(ESPHOME) compile $(CONFIG_ARDUINO)

# Builds the Node's firmware into .esphome/build/geopro-202s/. Needs secrets.yaml next to
# geopro.yaml; the one dummy-secrets writes is enough to build, not to flash.
compile-node: esphome-version
	$(ESPHOME) compile $(NODE_CONFIG)

clean:
	rm -rf $(BUILD_DIR)
