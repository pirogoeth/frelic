#include "sockmon.h"

#include <errno.h>

ssize_t write(int fd, const void *buf, size_t count) {
    // Check if we've gotten a copy of the write() syscall. If not,
    // use dlsym() to grab it.
    if (_libc_write == NULL) {
        _libc_write = dlsym(RTLD_NEXT, "write");
    }

    printf(
            " write(fdesc %d, '%s')\n",
            fd,
            (unsigned char *) buf
    );

    return _libc_write(fd, buf, count);
}

ssize_t read(int fd, const void *buf, size_t count) {
    // Check if we've gotten a copy of the read() syscall. If not,
    // use dlsym() to grab it.
    if (_libc_read == NULL) {
        _libc_read = dlsym(RTLD_NEXT, "read");
    }

    printf(
            " read(fdesc %d, %lu bytes)",
            fd,
            count
    );

    int rc = _libc_read(fd, buf, count);
    if (rc == -1) {
        printf(
                " = %d, %s\n",
                errno,
                strerror(errno)
        );
        return rc;
    } else {
        printf(
                " = '%s'\n",
                buf
        );
        return rc;
    }
}
