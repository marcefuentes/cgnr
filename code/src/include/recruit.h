#ifndef RECRUIT_H
#define RECRUIT_H

#include "individual.h"

struct Recruit {
    double          randomwc;
    double          qBDefault;
    double          ChooseGrain;
    double          Choose_ltGrain;
    double          MimicGrain;
    double          ImimicGrain;
    double          Imimic_ltGrain;
    double          cost;
    struct Recruit *next;
};

// Functions for handling recruits
struct Recruit *create_recruits(unsigned int deaths, double w_cumulative);
void            free_recruit_list(struct Recruit **head);
void            kill(struct Recruit *recruit, struct Individual *ind_first, unsigned int population_size);

#endif  // RECRUIT_H
