#include "stats.h"

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

void stats_end_of_simulation(struct Stats *stats, struct Stats *statsall, unsigned int periods) {
    // Globals and time
    for (unsigned int period = 0; period < periods; period++, stats++, statsall++) {
        statsall->alpha = stats->alpha;
        statsall->logES = stats->logES;
        statsall->Given = stats->Given;
        statsall->time = stats->time;

        // Continous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Bins
            for (int bin = 0; bin < BINS; bin++) {
                statsall->frc[variable][bin] += stats->frc[variable][bin];
                statsall->frc2[variable][bin] += stats->frc[variable][bin] * stats->frc[variable][bin];
            }

            // Quartiles
            statsall->median[variable] += stats->median[variable];
            statsall->iqr[variable] += stats->iqr[variable];
            statsall->mean[variable] += stats->mean[variable];
            statsall->sd[variable] += stats->sd[variable];
            statsall->median2[variable] += stats->median[variable] * stats->median[variable];
            statsall->iqr2[variable] += stats->iqr[variable] * stats->iqr[variable];
            statsall->mean2[variable] += stats->mean[variable] * stats->mean[variable];
            statsall->sd2[variable] += stats->sd[variable] * stats->sd[variable];
        }

        // Correlations
        for (int pair = 0; pair < PAIRS; pair++) {
            statsall->corr[pair] += stats->corr[pair];
            statsall->corr2[pair] += stats->corr[pair] * stats->corr[pair];
        }
    }
}

void stats_period(struct Individual *ind, struct Individual *ind_last, struct Stats *stats,
                  unsigned int population_size) {
    int    count[CONTINUOUS_VARS][BINS] = {{0}};
    double bin_size[CONTINUOUS_VARS];
    for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
        bin_size[variable] = 1.0 / BINS;
        stats->mean[variable] = 0.0;
        stats->sd[variable] = 0.0;
    }

    int correlationPairs[PAIRS][2] = {
        {VARIABLE_Q_B_SEEN, VARIABLE_CHOOSE_GRAIN},        {VARIABLE_Q_B_SEEN, VARIABLE_CHOOSE_LT_GRAIN},
        {VARIABLE_Q_B_SEEN, VARIABLE_MIMIC_GRAIN},         {VARIABLE_Q_B_SEEN, VARIABLE_IMIMIC_GRAIN},
        {VARIABLE_Q_B_SEEN, VARIABLE_IMIMIC_LT_GRAIN},     {VARIABLE_CHOOSE_GRAIN, VARIABLE_CHOOSE_LT_GRAIN},
        {VARIABLE_CHOOSE_GRAIN, VARIABLE_MIMIC_GRAIN},     {VARIABLE_CHOOSE_GRAIN, VARIABLE_IMIMIC_GRAIN},
        {VARIABLE_CHOOSE_GRAIN, VARIABLE_IMIMIC_LT_GRAIN}, {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_MIMIC_GRAIN},
        {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_IMIMIC_GRAIN}, {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_IMIMIC_LT_GRAIN},
        {VARIABLE_MIMIC_GRAIN, VARIABLE_IMIMIC_GRAIN},     {VARIABLE_MIMIC_GRAIN, VARIABLE_IMIMIC_LT_GRAIN},
        {VARIABLE_IMIMIC_GRAIN, VARIABLE_IMIMIC_LT_GRAIN}};

    for (int pair = 0; pair < PAIRS; pair++) {
        stats->corr[pair] = 0.0;
    }

    for (; ind < ind_last; ind++) {
        double *continuous_vars[CONTINUOUS_VARS] = {&ind->w,           &ind->qBDefault,      &ind->qBSeen,
                                                    &ind->ChooseGrain, &ind->Choose_ltGrain, &ind->MimicGrain,
                                                    &ind->ImimicGrain, &ind->Imimic_ltGrain};

        // Continous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Bins
            count[variable][select_bin(bin_size[variable], *continuous_vars[variable])]++;
            // Mean and standard deviation
            stats->mean[variable] += *continuous_vars[variable];
            stats->sd[variable] += *continuous_vars[variable] * *continuous_vars[variable];
        }

        // Correlations
        stats->corr[CORR_Q_B_SEEN_CHOOSE_GRAIN] += ind->qBSeen * ind->ChooseGrain;
        stats->corr[CORR_Q_B_SEEN_CHOOSE_LT_GRAIN] += ind->qBSeen * ind->Choose_ltGrain;
        stats->corr[CORR_Q_B_SEEN_MIMIC_GRAIN] += ind->qBSeen * ind->MimicGrain;
        stats->corr[CORR_Q_B_SEEN_IMIMIC_GRAIN] += ind->qBSeen * ind->ImimicGrain;
        stats->corr[CORR_Q_B_SEEN_IMIMIC_LT_GRAIN] += ind->qBSeen * ind->Imimic_ltGrain;
        stats->corr[CORR_CHOOSE_GRAIN_CHOOSE_LT_GRAIN] += ind->ChooseGrain * ind->Choose_ltGrain;
        stats->corr[CORR_CHOOSE_GRAIN_MIMIC_GRAIN] += ind->ChooseGrain * ind->MimicGrain;
        stats->corr[CORR_CHOOSE_GRAIN_IMIMIC_GRAIN] += ind->ChooseGrain * ind->ImimicGrain;
        stats->corr[CORR_CHOOSE_GRAIN_IMIMIC_LT_GRAIN] += ind->ChooseGrain * ind->Imimic_ltGrain;
        stats->corr[CORR_CHOOSE_LT_GRAIN_MIMIC_GRAIN] += ind->Choose_ltGrain * ind->MimicGrain;
        stats->corr[CORR_CHOOSE_LT_GRAIN_IMIMIC_GRAIN] += ind->Choose_ltGrain * ind->ImimicGrain;
        stats->corr[CORR_CHOOSE_LT_GRAIN_IMIMIC_LT_GRAIN] += ind->Choose_ltGrain * ind->Imimic_ltGrain;
        stats->corr[CORR_MIMIC_GRAIN_IMIMIC_GRAIN] += ind->MimicGrain * ind->ImimicGrain;
        stats->corr[CORR_MIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->MimicGrain * ind->Imimic_ltGrain;
        stats->corr[CORR_IMIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->ImimicGrain * ind->Imimic_ltGrain;
    }

    // Correlations
    for (int pair = 0; pair < PAIRS; pair++) {
        stats->corr[pair] =
            pearson_r(stats->mean[correlationPairs[pair][0]], stats->mean[correlationPairs[pair][1]], stats->corr[pair],
                      stats->sd[correlationPairs[pair][0]], stats->sd[correlationPairs[pair][1]], population_size);
    }

    // Continous variables
    for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
        // Bins
        for (int bin = 0; bin < BINS; bin++) {
            stats->frc[variable][bin] = (double)count[variable][bin] / population_size;
        }

        // Quartiles
        int    bin = 0;
        double previousfreq = 0.0;

        double lower_quartile = quartile(stats->frc[variable], BINS, LOWER_QUARTILE, &bin, &previousfreq);
        double median = quartile(stats->frc[variable], BINS, MEDIAN, &bin, &previousfreq);
        double upper_quartile = quartile(stats->frc[variable], BINS, UPPER_QUARTILE, &bin, &previousfreq);
        stats->median[variable] = median;
        stats->iqr[variable] = upper_quartile - lower_quartile;

        // Mean and standard deviation
        stats->sd[variable] = stdev(stats->mean[variable], stats->sd[variable], population_size);
        stats->mean[variable] = stats->mean[variable] / population_size;
    }
}
