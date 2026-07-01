# Build and run every proof from the committed C -- with nothing but a C compiler.
# No ErnosPlain needed. Each test_*.c is the self-contained output of the ErnosPlain
# compiler for one proof; it includes its own runtime and uses only standard headers.
#
#   make            build every proof
#   make check      build every proof, run it, and report ok / FAIL
#   make clean      remove the built binaries

CC ?= cc
CFLAGS ?= -O2
SOURCES := $(wildcard test_*.c)
BINARIES := $(SOURCES:.c=)

all: $(BINARIES)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

check: all
	@fail=0; \
	for b in $(BINARIES); do \
	  out="$$(./$$b)"; rc=$$?; \
	  if [ $$rc -ne 0 ]; then \
	    echo "FAIL  $$b (exit $$rc)"; fail=1; \
	  elif printf '%s\n' "$$out" | grep -q FAIL; then \
	    echo "FAIL  $$b"; fail=1; \
	  else \
	    echo "ok    $$b"; \
	  fi; \
	done; \
	if [ $$fail -eq 0 ]; then \
	  echo "-------------------------------------------"; \
	  echo "ALL PROOFS PASS"; \
	else \
	  echo "SOME PROOFS FAILED"; exit 1; \
	fi

clean:
	rm -f $(BINARIES)

.PHONY: all check clean
