# Makefile for building test libraries and applications
# This creates a realistic scenario for testing library path fixing

CC = gcc
CFLAGS = -Wall -fPIC
LDFLAGS = -shared

LIB_DIR = custom_libs
PLUGIN_DIR = plugins
BIN_DIR = bin

MATH_VERSION = 1.2.3
STRING_VERSION = 2.0.1

.PHONY: all clean directories setup test

all: directories libraries applications plugins

directories:
	@mkdir -p $(LIB_DIR)
	@mkdir -p $(PLUGIN_DIR)
	@mkdir -p $(BIN_DIR)

libraries: directories
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(LIB_DIR)/libmath_utils.so.$(MATH_VERSION) libmath_utils.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(LIB_DIR)/libstring_utils.so.$(STRING_VERSION) libstring_utils.c
	# Create version symlinks
	cd $(LIB_DIR) && ln -sf libmath_utils.so.$(MATH_VERSION) libmath_utils.so.1
	cd $(LIB_DIR) && ln -sf libmath_utils.so.1 libmath_utils.so
	cd $(LIB_DIR) && ln -sf libstring_utils.so.$(STRING_VERSION) libstring_utils.so.2
	cd $(LIB_DIR) && ln -sf libstring_utils.so.2 libstring_utils.so

applications: libraries
	$(CC) $(CFLAGS) -o $(BIN_DIR)/myapp test_app.c \
		-L$(LIB_DIR) -lmath_utils -lstring_utils
	$(CC) $(CFLAGS) -o $(BIN_DIR)/plugin_system plugin_system.c -ldl

plugins: libraries
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(PLUGIN_DIR)/plugin_logger.so plugin_logger.c \
		-L$(LIB_DIR) -lstring_utils
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(PLUGIN_DIR)/plugin_calculator.so plugin_calculator.c \
		-L$(LIB_DIR) -lmath_utils

setup: all
	@echo ""
	@echo "=== Build Complete ==="
	@echo "Binaries created with missing library paths for testing."
	@echo ""
	@echo "Structure:"
	@echo "  $(BIN_DIR)/myapp             - Main application"
	@echo "  $(BIN_DIR)/plugin_system     - Plugin loader"
	@echo "  $(LIB_DIR)/*.so              - Custom libraries"
	@echo "  $(PLUGIN_DIR)/*.so           - Plugins"
	@echo ""
	@echo "To test library dependencies:"
	@echo "  ldd $(BIN_DIR)/myapp"
	@echo "  ldd $(PLUGIN_DIR)/plugin_logger.so"
	@echo ""

# Test that libraries are missing (before fix)
test: all
	@echo "=== Testing library dependencies (should show missing libs) ==="
	@echo ""
	@echo "Main application:"
	-@ldd $(BIN_DIR)/myapp | grep "not found" || echo "  [Libraries found - unexpected!]"
	@echo ""
	@echo "Plugin loader:"
	-@ldd $(BIN_DIR)/plugin_system
	@echo ""
	@echo "Logger plugin:"
	-@ldd $(PLUGIN_DIR)/plugin_logger.so | grep "not found" || echo "  [Libraries found - unexpected!]"
	@echo ""
	@echo "Calculator plugin:"
	-@ldd $(PLUGIN_DIR)/plugin_calculator.so | grep "not found" || echo "  [Libraries found - unexpected!]"
	@echo ""

clean:
	rm -rf $(LIB_DIR) $(PLUGIN_DIR) $(BIN_DIR)
	rm -f *.o