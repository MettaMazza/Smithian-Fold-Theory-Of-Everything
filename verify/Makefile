# Build and run every proof from the committed C -- with nothing but a C compiler.
# No ErnosPlain needed. Each test_*.c is the self-contained output of the ErnosPlain
# compiler for one proof; it includes its own runtime and uses only standard headers.
#
#   make            build every proof
#   make check      build every proof, run it, and report ok / FAIL per suite
#   make prove      run the unified driver: enumerate EVERY forced value + grand tally
#   make online     cross-check forced values against LIVE-fetched NIST CODATA
#   make uniqueness  the alpha assembly is the UNIQUE 9-digit hit over the smooth space
#   make clean      remove the built binaries

CC ?= cc
CFLAGS ?= -O2
NPROC := $(shell getconf _NPROCESSORS_ONLN 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
MAKEFLAGS += -j$(NPROC)
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

prove: all
	@sh prove_parallel.sh

prove-serial: all
	@sh prove_all.sh

online:
	@python3 online_codata_check.py

uniqueness:
	@python3 uniqueness_search.py

clean:
	rm -f $(BINARIES)

.PHONY: all check prove prove-serial online uniqueness clean
