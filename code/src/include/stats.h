#ifndef STATS_H
#define STATS_H

#include "individual.h"

enum { BINS = 64, CONTINUOUS_VARS = 8, PAIRS = 15 };

typedef struct Stats {
    double        alpha;
    double        logES;
    double        Given;
    unsigned long time;
    double        mean[CONTINUOUS_VARS];
    double        mean2[CONTINUOUS_VARS];
    double        sd[CONTINUOUS_VARS];
    double        sd2[CONTINUOUS_VARS];
    double        frc[CONTINUOUS_VARS][BINS];
    double        frc2[CONTINUOUS_VARS][BINS];
    double        median[CONTINUOUS_VARS];
    double        median2[CONTINUOUS_VARS];
    double        iqr[CONTINUOUS_VARS];
    double        iqr2[CONTINUOUS_VARS];
    double        corr[PAIRS];
    double        corr2[PAIRS];
} Stats;

// Functions for handling statistics
int  stats_csv(Stats *stats, unsigned int periods, unsigned int runs, char *filename);
int  stats_frq(Stats *stats, unsigned int periods, unsigned int runs, char *filename);
void stats_period(Individual *ind, Individual *ind_last, Stats *stats, unsigned int population_size);

#endif  // STATS_H
