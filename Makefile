CC=gcc

CFLAGS=-Wall -Wextra
DEBUGFLAGS=-g -fsanitize=address
RELEASEFLAGS=-O2 -DNDEBUG

ifdef DEBUG
CFLAGS += $(DEBUGFLAGS)
else
CFLAGS += $(RELEASEFLAGS)
endif

all: busy verybusy

.PHONY: clean

busy: busy.c
	$(CC) $(CFLAGS) $^ -o $@

verybusy: verybusy.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -f busy
	rm -f verybusy
