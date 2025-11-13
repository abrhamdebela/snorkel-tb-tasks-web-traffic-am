# Root Makefile: jobserver-aware recursion, distcc/ccache friendly.

include config.mk

SUBDIRS := cpp src tests

.PHONY: all libs clean test rebuild cpp-lib src-lib src-bin $(SUBDIRS)

# Top-level parallel-safe targets
all: cpp-lib src-lib src-bin

cpp-lib:
	+@$(MAKE) -C cpp all

src-lib: cpp-lib
	+@$(MAKE) -C src lib

src-bin: src-lib
	+@$(MAKE) -C src all

libs: cpp-lib src-lib

test: all
	+@$(MAKE) -C tests test

# Clean before rebuild to avoid parallel delete/compile race
rebuild: clean all test

clean:
	@for d in $(SUBDIRS); do $(MAKE) -C $$d clean; done
	@$(RM) -r build

# Environment diagnostic
print-%:
	@echo '$*=$($*)'
