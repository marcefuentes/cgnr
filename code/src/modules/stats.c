#include "stats.h"

#include "individual.h"
#include "math_tools.h"

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

static const double BIN_SIZE = 1.0 / BINS;
static const double LOWER_QUARTILE = 0.25;
static const double MEDIAN = 0.50;
static const double UPPER_QUARTILE = 0.75;
static const int    correlationPairs[PAIRS][2] = {
    {VARIABLE_Q_B_SEEN, VARIABLE_CHOOSE_GRAIN},        {VARIABLE_Q_B_SEEN, VARIABLE_CHOOSE_LT_GRAIN},
    {VARIABLE_Q_B_SEEN, VARIABLE_MIMIC_GRAIN},         {VARIABLE_Q_B_SEEN, VARIABLE_IMIMIC_GRAIN},
    {VARIABLE_Q_B_SEEN, VARIABLE_IMIMIC_LT_GRAIN},     {VARIABLE_CHOOSE_GRAIN, VARIABLE_CHOOSE_LT_GRAIN},
    {VARIABLE_CHOOSE_GRAIN, VARIABLE_MIMIC_GRAIN},     {VARIABLE_CHOOSE_GRAIN, VARIABLE_IMIMIC_GRAIN},
    {VARIABLE_CHOOSE_GRAIN, VARIABLE_IMIMIC_LT_GRAIN}, {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_MIMIC_GRAIN},
    {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_IMIMIC_GRAIN}, {VARIABLE_CHOOSE_LT_GRAIN, VARIABLE_IMIMIC_LT_GRAIN},
    {VARIABLE_MIMIC_GRAIN, VARIABLE_IMIMIC_GRAIN},     {VARIABLE_MIMIC_GRAIN, VARIABLE_IMIMIC_LT_GRAIN},
    {VARIABLE_IMIMIC_GRAIN, VARIABLE_IMIMIC_LT_GRAIN}};

void stats_period(struct Individual *ind, struct Individual *ind_last, struct Stats *stats_all_runs,
                  unsigned int population_size) {
    struct Stats stats;
    int          count[CONTINUOUS_VARS][BINS] = {{0}};

    for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
        stats.sum[variable] = 0.0;
        stats.sum2[variable] = 0.0;
    }

    for (int pair = 0; pair < PAIRS; pair++) {
        stats.sum_xy[pair] = 0.0;
    }

    for (; ind < ind_last; ind++) {
        const double *const continuous_vars[CONTINUOUS_VARS] = {
            &ind->w,          &ind->qBDefault,   &ind->qBSeen,        &ind->ChooseGrain, &ind->Choose_ltGrain,
            &ind->MimicGrain, &ind->ImimicGrain, &ind->Imimic_ltGrain};

        // Continous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Bins
            count[variable][select_bin(BIN_SIZE, *continuous_vars[variable])]++;

            // Mean and standard deviation
            stats.sum[variable] += *continuous_vars[variable];
            stats.sum2[variable] += *continuous_vars[variable] * *continuous_vars[variable];
        }

        // Correlations
        stats.sum_xy[CORR_Q_B_SEEN_CHOOSE_GRAIN] += ind->qBSeen * ind->ChooseGrain;
        stats.sum_xy[CORR_Q_B_SEEN_CHOOSE_LT_GRAIN] += ind->qBSeen * ind->Choose_ltGrain;
        stats.sum_xy[CORR_Q_B_SEEN_MIMIC_GRAIN] += ind->qBSeen * ind->MimicGrain;
        stats.sum_xy[CORR_Q_B_SEEN_IMIMIC_GRAIN] += ind->qBSeen * ind->ImimicGrain;
        stats.sum_xy[CORR_Q_B_SEEN_IMIMIC_LT_GRAIN] += ind->qBSeen * ind->Imimic_ltGrain;
        stats.sum_xy[CORR_CHOOSE_GRAIN_CHOOSE_LT_GRAIN] += ind->ChooseGrain * ind->Choose_ltGrain;
        stats.sum_xy[CORR_CHOOSE_GRAIN_MIMIC_GRAIN] += ind->ChooseGrain * ind->MimicGrain;
        stats.sum_xy[CORR_CHOOSE_GRAIN_IMIMIC_GRAIN] += ind->ChooseGrain * ind->ImimicGrain;
        stats.sum_xy[CORR_CHOOSE_GRAIN_IMIMIC_LT_GRAIN] += ind->ChooseGrain * ind->Imimic_ltGrain;
        stats.sum_xy[CORR_CHOOSE_LT_GRAIN_MIMIC_GRAIN] += ind->Choose_ltGrain * ind->MimicGrain;
        stats.sum_xy[CORR_CHOOSE_LT_GRAIN_IMIMIC_GRAIN] += ind->Choose_ltGrain * ind->ImimicGrain;
        stats.sum_xy[CORR_CHOOSE_LT_GRAIN_IMIMIC_LT_GRAIN] += ind->Choose_ltGrain * ind->Imimic_ltGrain;
        stats.sum_xy[CORR_MIMIC_GRAIN_IMIMIC_GRAIN] += ind->MimicGrain * ind->ImimicGrain;
        stats.sum_xy[CORR_MIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->MimicGrain * ind->Imimic_ltGrain;
        stats.sum_xy[CORR_IMIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->ImimicGrain * ind->Imimic_ltGrain;
    }

    // Continous variables
    for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
        // Bins
        for (int bin = 0; bin < BINS; bin++) {
            double frc = (double)count[variable][bin] / population_size;
            stats_all_runs->frc[variable][bin] += frc;
            stats_all_runs->frc2[variable][bin] += frc * frc;
            stats.frc[variable][bin] = frc;  // For quartiles
        }

        // Quartiles
        int    bin = 0;
        double previousfreq = 0.0;

        double lower_quartile = quartile(stats.frc[variable], BINS, LOWER_QUARTILE, &bin, &previousfreq);
        double median = quartile(stats.frc[variable], BINS, MEDIAN, &bin, &previousfreq);
        double upper_quartile = quartile(stats.frc[variable], BINS, UPPER_QUARTILE, &bin, &previousfreq);
        stats_all_runs->median[variable] += median;
        stats_all_runs->median2[variable] += median * median;
        double iqr = upper_quartile - lower_quartile;
        stats_all_runs->iqr[variable] += iqr;
        stats_all_runs->iqr2[variable] += iqr * iqr;

        // Mean and standard deviation
        double mean = stats.sum[variable] / population_size;
        stats_all_runs->mean[variable] += mean;
        stats_all_runs->mean2[variable] += mean * mean;
        double st_dev = stdev(stats.sum[variable], stats.sum2[variable], population_size);
        stats_all_runs->sd[variable] += st_dev;
        stats_all_runs->sd2[variable] += st_dev * st_dev;
    }

    // Correlations
    for (int pair = 0; pair < PAIRS; pair++) {
        int    var_x = correlationPairs[pair][0];
        int    var_y = correlationPairs[pair][1];
        double corr = pearson_r(stats.sum[var_x], stats.sum[var_y], stats.sum_xy[pair], stats.sum2[var_x],
                                stats.sum2[var_y], population_size);
        stats_all_runs->corr[pair] += corr;
        stats_all_runs->corr2[pair] += corr * corr;
    }
}
