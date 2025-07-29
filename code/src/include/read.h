#ifndef READ_H
#define READ_H

#include "globals.h"

int initialize_rng(Globals *globals);
int calculate_derived_globals(Globals *globals);
int read_globals(const char *filename, Globals *globals);

#endif /* READ_H */
