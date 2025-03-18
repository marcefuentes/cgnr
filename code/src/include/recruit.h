#ifndef RECRUIT_H
#define RECRUIT_H

#include "individual.h"

typedef struct Recruit {
    double          randomwc;
    double          qBDefault;
    double          ChooseGrain;
    double          Choose_ltGrain;
    double          MimicGrain;
    double          ImimicGrain;
    double          Imimic_ltGrain;
    double          cost;
    struct Recruit *next;
} Recruit;

// Functions for handling recruits
Recruit *create_recruits(unsigned int deaths, double w_cumulative);
void     free_recruit_list(Recruit **head);
void     kill(Recruit *recruit_first, Individual *ind_first, unsigned int population_size);
void     mutate(Recruit *recruit_first, Individual *ind_first, double qb_mutation_size, double grain_mutation_size,
                double cost, int language);

#endif  // RECRUIT_H
