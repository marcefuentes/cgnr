#include <stdio.h>

#include "io.h"

int file_write_error(char *filename) {
    fprintf(stderr, "Failed to open file %s for writing.\n", filename);
    return -1;
}
