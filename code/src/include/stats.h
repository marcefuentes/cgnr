#ifndef STATS_H
#define STATS_H

#include "individual.h"

enum { BINS = 64, CONTINUOUS_VARS = 8, PAIRS = 15 };

struct Stats {
    unsigned long time;
    double        alpha, logES, Given;
    double        mean[CONTINUOUS_VARS], mean2[CONTINUOUS_VARS];
    double        sd[CONTINUOUS_VARS], sd2[CONTINUOUS_VARS];
    double        frc[CONTINUOUS_VARS][BINS], frc2[CONTINUOUS_VARS][BINS];
    double        median[CONTINUOUS_VARS], median2[CONTINUOUS_VARS];
    double        iqr[CONTINUOUS_VARS], iqr2[CONTINUOUS_VARS];
    double        corr[PAIRS], corr2[PAIRS];
};

// Functions for handling statistics
int  stats_csv(struct Stats *statsall, struct Stats *statsall_last, unsigned int runs, char *filename);
int  stats_frq(struct Stats *statsall, struct Stats *statsall_last, unsigned int runs, char *filename);
void stats_end_of_simulation(struct Stats *stats, struct Stats *stats_last, struct Stats *statsall);
void stats_period(struct Individual *ind, struct Individual *ind_last, struct Stats *stats,
                  unsigned int population_size);

#endif  // STATS_H
