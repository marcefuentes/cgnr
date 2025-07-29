#ifndef INDIVIDUAL_H
#define INDIVIDUAL_H

#include <gsl/gsl_rng.h>

#include "globals.h"

typedef struct Individual {
    unsigned int       age;
    double             qBDefault;
    double             qBDecided;
    double             qBSeen;
    double             qBSeenSum;
    double             qBSeen_lt;
    double             ChooseGrain;
    double             Choose_ltGrain;
    double             MimicGrain;
    double             ImimicGrain;
    double             Imimic_ltGrain;
    double             cost;
    double             w;
    double             wCumulative;
    struct Individual *oldpartner;
    struct Individual *partner;
} Individual;

#define INITIAL_INDIVIDUAL               \
    ((Individual){.age = 0,              \
                  .qBDefault = 0.1,      \
                  .qBDecided = 0.1,      \
                  .qBSeen = 0.1,         \
                  .qBSeenSum = 0.0,      \
                  .qBSeen_lt = 0.0,      \
                  .ChooseGrain = 1.0,    \
                  .Choose_ltGrain = 1.0, \
                  .MimicGrain = 1.0,     \
                  .ImimicGrain = 1.0,    \
                  .Imimic_ltGrain = 1.0, \
                  .cost = 0.0,           \
                  .w = 0.0,              \
                  .wCumulative = 0.0,    \
                  .oldpartner = NULL,    \
                  .partner = NULL})

int    choose_partner(Individual *ind_first, Individual *ind_last, unsigned int group_size, gsl_rng *rng);
void   decide_qB(Individual *ind_first, Individual *ind_last, int indirect_r);
double fitness(Individual *ind_first, Individual *ind_last, double given, double alpha, double rho);
int    handle_recruitment(Individual *ind_first, Individual *ind_last, double w_cumulative, Globals *globals);
void   initial_pairs(Individual *ind_first, Individual *ind_last);
int    shuffle_partners(Individual *ind_first, Individual *ind_last, unsigned int group_size, gsl_rng *rng);
void   update_scores(Individual *ind_first, Individual *ind_last);

#endif  // INDIVIDUAL_H
