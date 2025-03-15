#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "globals.h"

struct GlobalVariables globals;

int read_key_value(FILE *file, const char *expected_key, void *value, const char *type);

int read_globals(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Failed to open file %s for reading.\n", filename);
        return -1;
    }

    if (read_key_value(file, "Seed", &globals.seed, "int") ||
        read_key_value(file, "N", &globals.population_size, "unsigned int") ||
        read_key_value(file, "Runs", &globals.runs, "unsigned int") ||
        read_key_value(file, "Time", &globals.time, "unsigned long") ||
        read_key_value(file, "Periods", &globals.periods, "unsigned int") ||
        read_key_value(file, "qBMutationSize", &globals.qb_mutation_size, "double") ||
        read_key_value(file, "GrainMutationSize", &globals.grain_mutation_size, "double") ||
        read_key_value(file, "DeathRate", &globals.death_rate, "double") ||
        read_key_value(file, "GroupSize", &globals.group_size, "unsigned int") ||
        read_key_value(file, "Cost", &globals.cost, "double") ||
        read_key_value(file, "PartnerChoice", &globals.partner_choice, "int") ||
        read_key_value(file, "Reciprocity", &globals.reciprocity, "int") ||
        read_key_value(file, "IndirectR", &globals.indirect_r, "int") ||
        read_key_value(file, "Language", &globals.language, "int") ||
        read_key_value(file, "Shuffle", &globals.shuffle, "int") ||
        read_key_value(file, "alpha", &globals.alpha, "double") ||
        read_key_value(file, "logES", &globals.loges, "double") ||
        read_key_value(file, "Given", &globals.given, "double")) {
        fprintf(stderr, "Failed to read globals from file %s.\n", filename);
        fclose(file);
        return -1;
    }

    fclose(file);

    globals.population_size = (unsigned int)(pow(2.0, (double)globals.population_size) + 0.5);
    globals.time = (unsigned long)(pow(2.0, (double)globals.time) + 0.5);
    globals.periods = (unsigned int)(pow(2.0, (double)globals.periods) + 0.5);
    globals.qb_mutation_size = pow(2.0, globals.qb_mutation_size);
    globals.grain_mutation_size = pow(2.0, globals.grain_mutation_size);
    globals.death_rate = pow(2.0, globals.death_rate);
    globals.group_size = (unsigned int)(pow(2.0, (double)globals.group_size) + 0.5);
    globals.cost = pow(2.0, globals.cost);
    globals.rho = 1.0 - 1.0 / pow(2.0, globals.loges);
    globals.time_per_period = globals.time / globals.periods;

    return 0;
}

int read_key_value(FILE *file, const char *expected_key, void *value, const char *type) {
    char line[128];
    char key[64];
    char val[64];

    if (fgets(line, sizeof(line), file) == NULL) {
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
