include ../config.mk

ROOT    := $(abspath ..)
OBJDIR  := $(abspath build)
LIBDIR  := $(OBJDIR)/lib
LIB     := $(LIBDIR)/libcpphash.a
SRCS    := hash.cpp
OBJS    := $(addprefix $(OBJDIR)/,$(notdir $(SRCS:.cpp=.o)))
DEPS    := $(OBJS:.o=.d)

.PHONY: all clean

all: $(LIB)

$(LIB): $(OBJS) | $(LIBDIR)
	ar rcs $@ $^

$(OBJDIR)/%.o: %.cpp | $(OBJDIR)
	@mkdir -p $(OBJDIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(LIBDIR):
	@mkdir -p $(LIBDIR)

$(OBJDIR):
	@mkdir -p $(OBJDIR)

clean:
	$(RM) -r $(OBJDIR) $(ROOT)/build/lib/libcpphash.a

-include $(DEPS)
