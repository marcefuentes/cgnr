#ifndef STATS_H
#define STATS_H

#include "individual.h"

enum { BINS = 64, CONTINUOUS_V = 8, PAIRS = 15 };

struct Stats {
    unsigned long time;
    double        alpha, logES, Given;
    double        mean[CONTINUOUS_V], mean2[CONTINUOUS_V];
    double        sd[CONTINUOUS_V], sd2[CONTINUOUS_V];
    double        frc[CONTINUOUS_V][BINS], frc2[CONTINUOUS_V][BINS];
    double        median[CONTINUOUS_V], median2[CONTINUOUS_V];
    double        iqr[CONTINUOUS_V], iqr2[CONTINUOUS_V];
    double        corr[PAIRS], corr2[PAIRS];
};

// Functions for handling statsregate statistics
int  stats_csv(struct Stats *statsall, struct Stats *statsall_last, unsigned int runs, char *filename);
int  stats_frq(struct Stats *statsall, struct Stats *statsall_last, unsigned int runs, char *filename);
void stats_end_of_simulation(struct Stats *stats, struct Stats *stats_last, struct Stats *statsall);
void stats_period(struct Individual *ind, struct Individual *ind_last, struct Stats *stats,
                  unsigned int population_size);

#endif  // AGGREGATE_H
