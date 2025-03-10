#ifndef AGGREGATE_H
#define AGGREGATE_H

#include "individual.h"  // Needed for stats functions using Individual

#define BINS 64
#define CONTINUOUS_V 8
#define PAIRS 15

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
void stats_end(struct Aggregate *agg, struct Aggregate *agg_last, struct Aggregate *aggall);
void stats_period(struct Individual *ind, struct Individual *ind_last, struct Aggregate *agg, unsigned int n);
void stats_runs(struct Aggregate *aggall, struct Aggregate *aggall_last, unsigned int runs);

#endif
