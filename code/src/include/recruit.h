#ifndef RECRUIT_H
#define RECRUIT_H

#include "individual.h"

int handle_recruitment(Individual *ind_first, Individual *ind_last, unsigned int deaths, double w_cumulative,
                       double qb_mutation_size, double grain_mutation_size, double cost, int language,
                       unsigned int population_size);

#endif  // RECRUIT_H
