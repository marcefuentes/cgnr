#ifndef IO_H
#define IO_H

#include "individual.h"

enum { MAX_FILENAME_LEN = 22 };

// File I/O functions
int write_time_elapsed(char *filename, float time_elapsed);
int write_ics(char *filename, int sequence, float alpha, float loges, float given, unsigned long time,
              struct Individual *ind, struct Individual *ind_last);

#endif  // IO_H
