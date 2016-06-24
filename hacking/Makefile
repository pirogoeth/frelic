CC = /usr/bin/clang
CFLAGS = -g -fno-limit-debug-info -O3

.PHONY: all

all: build

build:
	$(CC) $(CFLAGS) -fPIC -shared -Wall -ldl -o sockmon.so sockmon.c

clean:
	@rm sockmon.so test

test: build
	$(CC) -g -fno-limit-debug-info -o test test.c
	LD_PRELOAD=$(PWD)/sockmon.so ./test
