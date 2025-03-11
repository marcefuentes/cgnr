#ifndef AGGREGATE_H
#define AGGREGATE_H

#include "individual.h"

enum { BINS = 64, CONTINUOUS_V = 8, PAIRS = 15 };

struct Aggregate {
    unsigned long time;
    double        alpha, logES, Given;
    double        mean[CONTINUOUS_V], mean2[CONTINUOUS_V];
    double        sd[CONTINUOUS_V], sd2[CONTINUOUS_V];
    double        frc[CONTINUOUS_V][BINS], frc2[CONTINUOUS_V][BINS];
    double        median[CONTINUOUS_V], median2[CONTINUOUS_V];
    double        iqr[CONTINUOUS_V], iqr2[CONTINUOUS_V];
    double        corr[PAIRS], corr2[PAIRS];
};

// Functions for handling aggregate statistics
void stats_end_of_simulation(struct Aggregate *agg, struct Aggregate *agg_last, struct Aggregate *aggall);
void stats_period(struct Individual *ind, struct Individual *ind_last, struct Aggregate *agg,
                  unsigned int population_size);
int  stats_csv(struct Aggregate *aggall, struct Aggregate *aggall_last, unsigned int runs, char *filename);
int  stats_frq(struct Aggregate *aggall, struct Aggregate *aggall_last, unsigned int runs, char *filename);

#endif  // AGGREGATE_H
