include ../config.mk

ROOT := $(abspath ..)
OBJDIR := $(abspath build)
LIBDIR := $(OBJDIR)/lib
BINDIR := $(OBJDIR)/bin
LIBCORE := $(LIBDIR)/libcore.a
BIN := $(BINDIR)/graphcli

CSRCS := graph.c minheap.c csv.c dijkstra.c cli.c
COBJS := $(addprefix $(OBJDIR)/,$(notdir $(CSRCS:.c=.o)))
CDEPS := $(COBJS:.o=.d)

CPPAPI := ../cpp/hash_c_api.h
CPPLIBDIR := $(ROOT)/cpp/build/lib

.PHONY: all lib clean

all: $(BIN)

lib: $(LIBCORE)

$(LIBCORE): $(OBJDIR)/graph.o $(OBJDIR)/minheap.o $(OBJDIR)/csv.o $(OBJDIR)/dijkstra.o | $(LIBDIR)
	ar rcs $@ $^

$(BIN): $(LIBCORE) $(OBJDIR)/cli.o | $(BINDIR)
	$(CC) $(CFLAGS) -o $@ $(OBJDIR)/cli.o \
		-L$(LIBDIR) -L$(CPPLIBDIR) -lcore -lcpphash

$(OBJDIR)/%.o: %.c $(CPPAPI) | $(OBJDIR)
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(LIBDIR):
	@mkdir -p $(LIBDIR)

$(BINDIR):
	@mkdir -p $(BINDIR)

$(OBJDIR):
	@mkdir -p $(OBJDIR)

clean:
	$(RM) -r $(OBJDIR)

-include $(CDEPS)
