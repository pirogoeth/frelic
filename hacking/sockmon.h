#ifndef SOCKMON_H
#define SOCKMON_H

// Define this so we get GNU features from imported headers.
#define _GNU_SOURCE

#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static ssize_t (*_libc_write)(int fd, const void *buf, size_t count) = NULL;
static ssize_t (*_libc_read)(int fd, const void *buf, size_t count) = NULL;

ssize_t write(int fd, const void *buf, size_t count);
ssize_t read(int fd, const void *buf, size_t count);

#endif
