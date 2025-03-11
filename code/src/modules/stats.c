#include <math.h>
#include <stdio.h>

#include "aggregate.h"
#include "individual.h"
#include "math_tools.h"

#define LOWER_QUARTILE 0.25
#define MEDIAN 0.50
#define UPPER_QUARTILE 0.75

enum {
    VARIABLE_W = 0,
    VARIABLE_Q_B_DEFAULT = 1,
    VARIABLE_Q_B_SEEN = 2,
    VARIABLE_CHOOSE_GRAIN = 3,
    VARIABLE_CHOOSE_LT_GRAIN = 4,
    VARIABLE_MIMIC_GRAIN = 5,
    VARIABLE_IMIMIC_GRAIN = 6,
    VARIABLE_IMIMIC_LT_GRAIN = 7
};

enum {
    CORR_Q_B_SEEN_CHOOSE_GRAIN = 0,
    CORR_Q_B_SEEN_CHOOSE_LT_GRAIN = 1,
    CORR_Q_B_SEEN_MIMIC_GRAIN = 2,
    CORR_Q_B_SEEN_IMIMIC_GRAIN = 3,
    CORR_Q_B_SEEN_IMIMIC_LT_GRAIN = 4,
    CORR_CHOOSE_GRAIN_CHOOSE_LT_GRAIN = 5,
    CORR_CHOOSE_GRAIN_MIMIC_GRAIN = 6,
    CORR_CHOOSE_GRAIN_IMIMIC_GRAIN = 7,
    CORR_CHOOSE_GRAIN_IMIMIC_LT_GRAIN = 8,
    CORR_CHOOSE_LT_GRAIN_MIMIC_GRAIN = 9,
    CORR_CHOOSE_LT_GRAIN_IMIMIC_GRAIN = 10,
    CORR_CHOOSE_LT_GRAIN_IMIMIC_LT_GRAIN = 11,
    CORR_MIMIC_GRAIN_IMIMIC_GRAIN = 12,
    CORR_MIMIC_GRAIN_IMIMIC_LT_GRAIN = 13,
    CORR_IMIMIC_GRAIN_IMIMIC_LT_GRAIN = 14
};

void stats_end_of_simulation(struct Aggregate *agg, struct Aggregate *agg_last, struct Aggregate *aggall) {
    for (; agg < agg_last; agg++, aggall++) {
        aggall->alpha = agg->alpha;
        aggall->logES = agg->logES;
        aggall->Given = agg->Given;
        aggall->time = agg->time;

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            for (int bin = 0; bin < BINS; bin++) {
                aggall->frc[variable][bin] += agg->frc[variable][bin];
                aggall->frc2[variable][bin] += agg->frc[variable][bin] * agg->frc[variable][bin];
            }

            aggall->median[variable] += agg->median[variable];
            aggall->iqr[variable] += agg->iqr[variable];
            aggall->mean[variable] += agg->mean[variable];
            aggall->sd[variable] += agg->sd[variable];
            aggall->median2[variable] += agg->median[variable] * agg->median[variable];
            aggall->iqr2[variable] += agg->iqr[variable] * agg->iqr[variable];
            aggall->mean2[variable] += agg->mean[variable] * agg->mean[variable];
            aggall->sd2[variable] += agg->sd[variable] * agg->sd[variable];
        }

        for (int pair = 0; pair < PAIRS; pair++) {
            aggall->corr[pair] += agg->corr[pair];
            aggall->corr2[pair] += agg->corr[pair] * agg->corr[pair];
        }
    }
}

void stats_period(struct Individual *ind, struct Individual *ind_last, struct Aggregate *agg,
                  unsigned int population_size) {
    int    count[CONTINUOUS_V][BINS] = {{0}};
    double bin_size[CONTINUOUS_V] = {1.0 / BINS, 1.0 / BINS, 1.0 / BINS, 1.0 / BINS,
                                     1.0 / BINS, 1.0 / BINS, 1.0 / BINS, 1.0 / BINS};
    int    correlationPairs[PAIRS][2] = {
        {VARIABLE_Q_B_SEEN, VARIABLE_CHOOSE_GRAIN},        {VARIABLE_Q_B_SEEN, VARIABLE_CHOOSE_LT_GRAIN},
        {VARIABLE_Q_B_SEEN, VARIABLE_MIMIC_GRAIN},         {VARIABLE_Q_B_SEEN, VARIABLE_IMIMIC_GRAIN},
        {VARIABLE_Q_B_SEEN, VARIABLE_IMIMIC_LT_GRAIN},     {VARIABLE_CHOOSE_GRAIN, VARIABLE_CHOOSE_LT_GRAIN},
        {VARIABLE_CHOOSE_GRAIN, VARIABLE_MIMIC_GRAIN},     {VARIABLE_CHOOSE_GRAIN, VARIABLE_IMIMIC_GRAIN},
        {VARIABLE_CHOOSE_GRAIN, VARIABLE_IMIMIC_LT_GRAIN}, {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_MIMIC_GRAIN},
        {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_IMIMIC_GRAIN}, {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_IMIMIC_LT_GRAIN},
        {VARIABLE_MIMIC_GRAIN, VARIABLE_IMIMIC_GRAIN},     {VARIABLE_MIMIC_GRAIN, VARIABLE_IMIMIC_LT_GRAIN},
        {VARIABLE_IMIMIC_GRAIN, VARIABLE_IMIMIC_LT_GRAIN}};

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        agg->mean[variable] = 0.0;
        agg->sd[variable] = 0.0;
    }

    for (int pair = 0; pair < PAIRS; pair++) {
        agg->corr[pair] = 0.0;
    }

    for (; ind < ind_last; ind++) {
        double *properties[CONTINUOUS_V] = {&ind->w,           &ind->qBDefault,      &ind->qBSeen,
                                            &ind->ChooseGrain, &ind->Choose_ltGrain, &ind->MimicGrain,
                                            &ind->ImimicGrain, &ind->Imimic_ltGrain};

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            count[variable][select_bin(bin_size[variable], *properties[variable])]++;
            agg->mean[variable] += *properties[variable];
            agg->sd[variable] += *properties[variable] * *properties[variable];
        }

        agg->corr[CORR_Q_B_SEEN_CHOOSE_GRAIN] += ind->qBSeen * ind->ChooseGrain;
        agg->corr[CORR_Q_B_SEEN_CHOOSE_LT_GRAIN] += ind->qBSeen * ind->Choose_ltGrain;
        agg->corr[CORR_Q_B_SEEN_MIMIC_GRAIN] += ind->qBSeen * ind->MimicGrain;
        agg->corr[CORR_Q_B_SEEN_IMIMIC_GRAIN] += ind->qBSeen * ind->ImimicGrain;
        agg->corr[CORR_Q_B_SEEN_IMIMIC_LT_GRAIN] += ind->qBSeen * ind->Imimic_ltGrain;
        agg->corr[CORR_CHOOSE_GRAIN_CHOOSE_LT_GRAIN] += ind->ChooseGrain * ind->Choose_ltGrain;
        agg->corr[CORR_CHOOSE_GRAIN_MIMIC_GRAIN] += ind->ChooseGrain * ind->MimicGrain;
        agg->corr[CORR_CHOOSE_GRAIN_IMIMIC_GRAIN] += ind->ChooseGrain * ind->ImimicGrain;
        agg->corr[CORR_CHOOSE_GRAIN_IMIMIC_LT_GRAIN] += ind->ChooseGrain * ind->Imimic_ltGrain;
        agg->corr[CORR_CHOOSE_LT_GRAIN_MIMIC_GRAIN] += ind->Choose_ltGrain * ind->MimicGrain;
        agg->corr[CORR_CHOOSE_LT_GRAIN_IMIMIC_GRAIN] += ind->Choose_ltGrain * ind->ImimicGrain;
        agg->corr[CORR_CHOOSE_LT_GRAIN_IMIMIC_LT_GRAIN] += ind->Choose_ltGrain * ind->Imimic_ltGrain;
        agg->corr[CORR_MIMIC_GRAIN_IMIMIC_GRAIN] += ind->MimicGrain * ind->ImimicGrain;
        agg->corr[CORR_MIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->MimicGrain * ind->Imimic_ltGrain;
        agg->corr[CORR_IMIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->ImimicGrain * ind->Imimic_ltGrain;
    }

    for (int pair = 0; pair < PAIRS; pair++) {
        agg->corr[pair] =
            pearson_r(agg->mean[correlationPairs[pair][0]], agg->mean[correlationPairs[pair][1]], agg->corr[pair],
                      agg->sd[correlationPairs[pair][0]], agg->sd[correlationPairs[pair][1]], population_size);
    }

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        for (int bin = 0; bin < BINS; bin++) {
            agg->frc[variable][bin] = (double)count[variable][bin] / population_size;
        }

        int    bin = 0;
        double previousfreq = 0.0;

        double lower_quartile = quartile(agg->frc[variable], BINS, LOWER_QUARTILE, &bin, &previousfreq);
        double median = quartile(agg->frc[variable], BINS, MEDIAN, &bin, &previousfreq);
        double upper_quartile = quartile(agg->frc[variable], BINS, UPPER_QUARTILE, &bin, &previousfreq);
        agg->median[variable] = median;
        agg->iqr[variable] = upper_quartile - lower_quartile;

        agg->sd[variable] = stdev(agg->mean[variable], agg->sd[variable], population_size);
        agg->mean[variable] = agg->mean[variable] / population_size;
    }
}
