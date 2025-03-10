#ifndef IO_H
#define IO_H

#include <stdio.h>

#include "aggregate.h"   // Needed for writing aggregate stats
#include "individual.h"  // Needed for writing individual data

#define MAX_FILENAME_LEN 22

// File I/O functions
int read_key_value(FILE *file_pointer, const char *expected_key, void *value, const char *type);

int write_headers_csv(char *filename);
int write_headers_frq(char *filename);
int write_stats_csv(char *filename, struct Aggregate *aggall, struct Aggregate *aggall_last);
int write_stats_frq(char *filename, struct Aggregate *aggall, struct Aggregate *aggall_last);
int write_time_elapsed(char *filename, float time_elapsed);
int write_ics(char *filename, int sequence, float alpha, float logES, float Given, unsigned long time,
              struct Individual *ind, struct Individual *ind_last);

#endif
