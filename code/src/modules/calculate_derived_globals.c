#include <math.h>

#include "globals.h"

int calculate_derived_globals(Globals *globals) {
    globals->population_size = (unsigned int)(pow(2.0, (double)globals->population_size) + 0.5);
    globals->time = (unsigned long)(pow(2.0, (double)globals->time) + 0.5);
    globals->periods = 1 + (unsigned int)(pow(2.0, (double)globals->periods) + 0.5);
    globals->qb_mutation_size = pow(2.0, globals->qb_mutation_size);
    globals->grain_mutation_size = pow(2.0, globals->grain_mutation_size);
    globals->death_rate = pow(2.0, globals->death_rate);
    globals->group_size = (unsigned int)(pow(2.0, (double)globals->group_size) + 0.5);
    globals->cost = pow(2.0, globals->cost);
    globals->rho = 1.0 - 1.0 / pow(2.0, globals->loges);
    globals->time_per_period = globals->time / (globals->periods - 1);
    return 0;
}
