#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sim.h"

int read_key_value(FILE *fp, const char *expected_key, void *value, const char *type) {
    char line[128];
    char key[64];
    char val[64];

    if (fgets(line, sizeof(line), fp) == NULL) {
        fprintf(stderr, "Unexpected end of file while reading %s.\n", expected_key);
        return -1;
    }

    if (sscanf(line, "%63[^,],%63s", key, val) != 2) {
        fprintf(stderr, "Failed to parse key-value pair from line %s.\n", line);
        return -1;
    }

    if (strcmp(key, expected_key) != 0) {
        fprintf(stderr, "Expected key '%s' but got '%s'.\n", expected_key, key);
        return -1;
    }

    if (strcmp(type, "int") == 0) {
        *((int *)value) = atoi(val);
    } else if (strcmp(type, "unsigned int") == 0) {
        *((unsigned int *)value) = (unsigned int)strtoul(val, NULL, 10);
    } else if (strcmp(type, "unsigned long") == 0) {
        *((unsigned long *)value) = strtoul(val, NULL, 10);
    } else if (strcmp(type, "double") == 0) {
        *((double *)value) = atof(val);
    } else {
        fprintf(stderr, "Invalid type '%s' for key-value pair.\n", type);
        return -1;
    }

    return 0;
}
