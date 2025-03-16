#ifndef IO_H
#define IO_H

#include "individual.h"

enum { MAX_ARG_LENGTH = 9, MAX_FILENAME_LEN = 22 };

// File I/O functions
int file_write_error(char *filename);
int write_time_elapsed(char *filename, float time_elapsed);
int write_ics(char *filename, unsigned int period, float alpha, float loges, float given, unsigned long time,
              struct Individual *ind, struct Individual *ind_last);

#endif  // IO_H
