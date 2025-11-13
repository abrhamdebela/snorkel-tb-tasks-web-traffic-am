include ../config.mk

ROOT := $(abspath ..)
BIN := $(BINDIR)/graph_tests
SRCS := test_graph.c
OBJS := $(patsubst %.c,build/%.o,$(SRCS))
DEPS := $(OBJS:.o=.d)

.PHONY: test clean all

all: $(BIN)

$(BIN): build/test_graph.o ../src/Makefile
	$(CC) $(CFLAGS) -o $@ $< \
		-L$(LIBDIR) -L$(ROOT)/src/build/lib -L$(ROOT)/build/lib \
		-lcore -lcpphash $(LDFLAGS) $(LDLIBS)

build/%.o: %.c | build
	$(CC) $(CFLAGS) -I../src -c $< -o $@

build:
	@mkdir -p build

test: all
	@echo "[tests] randomized correctness and edge cases"
	@$(BINDIR)/graph_tests

clean:
	$(RM) -r build $(BIN)

-include $(DEPS)
