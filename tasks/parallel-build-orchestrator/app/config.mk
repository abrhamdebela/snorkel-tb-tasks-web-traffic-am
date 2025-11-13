# Shared configuration for all subprojects

ROOT    := $(abspath $(CURDIR))
PREFIX  ?= $(ROOT)/build
BINDIR  := $(PREFIX)/bin
LIBDIR  := $(PREFIX)/lib
INCDIR  := $(ROOT)/include

CC      ?= gcc
CXX     ?= g++
CSTD    ?= gnu17
CXXSTD  ?= c++17

WARN_C   := -Wall -Wextra -Wpedantic -Werror -Wshadow -Wpointer-arith -Wcast-qual -Wwrite-strings -Wmissing-prototypes
WARN_CXX := -Wall -Wextra -Wpedantic -Werror -Wshadow

OPT ?= -O2
DBG ?= -g3

CFLAGS   ?= $(OPT) $(DBG) -std=$(CSTD) $(WARN_C)   -fno-omit-frame-pointer -fPIC -I$(INCDIR) -Isrc -MMD -MP
CXXFLAGS ?= $(OPT) $(DBG) -std=$(CXXSTD) $(WARN_CXX) -fno-omit-frame-pointer -fPIC -I$(INCDIR) -Icpp -MMD -MP
LDFLAGS  ?=
LDLIBS   ?=

# Create standard build dirs automatically
$(shell mkdir -p $(BINDIR) $(LIBDIR))
