#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int fd = open("/tmp/test.txt", O_RDWR | O_CREAT | O_TRUNC);

    char *data = "ayy lmao";

    ssize_t rc;
    rc = write(fd, data, strlen(data));
    if (rc == -1) {
        perror("Write failed");
        return -1;
    }

    rc = lseek(fd, 0L, SEEK_SET);
    if (rc == -1) {
        perror("Seek failed");
        return -1;
    }

    char *buf = (char *) malloc(256);
    rc = read(fd, buf, strlen(data));
    if (rc == -1) {
        perror("Read failed");
        return -1;
    }

    rc = close(fd);
    if (rc == -1) {
        perror("Close failed");
        return -1;
    }

    if (strncmp(buf, data, strlen(data)) == 0) {
        free(buf);
        printf("\n\nTest completed!\n");
        return 0;
    } else {
        printf("Original data: %s\n", (data));
        printf("Read data: %s\n", (buf));
        free(buf);
        return -1;
    }
}
