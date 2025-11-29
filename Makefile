# Picked from https://stackoverflow.com/questions/714100/os-detecting-makefile
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	BIN_FORMAT = elf64
	TARGET = x86_64-linux
endif
ifeq ($(UNAME_S),Darwin) # for mac
	BIN_FORMAT = macho64
	TARGET = x86_64-darwin
endif
export CFLAGS ?= -target $(TARGET) -g

PROGS := $(basename $(notdir $(wildcard progs/*.src)))
PYTHON := .venv/bin/python3
RUNS := $(addprefix progs/,$(addsuffix .run,$(PROGS)))

.PHONY: all-progs

all-progs: $(RUNS)

compile-one: 
	$(PYTHON) -m exec.run_compile $(SRC) > $(basename $(SRC)).s

progs/%.s: progs/%.src
	$(PYTHON) -m exec.run_compile $< > $@

progs/%.o: progs/%.s
	nasm -f $(BIN_FORMAT) -o $@ $<

progs/%.run: progs/%.o rt/sys.c
	clang -o $@ $(CFLAGS) rt/sys.c $<

clean:
	rm -f progs/*.s progs/*.o progs/*.run

interp-one:
	$(PYTHON) -m exec.run_interp $(SRC)