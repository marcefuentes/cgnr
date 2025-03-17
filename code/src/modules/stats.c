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

void stats_period(struct Individual *ind, struct Individual *ind_last, struct Stats *stats,
                  unsigned int population_size) {
    int    count[CONTINUOUS_VARS][BINS] = {{0}};
    double freq[CONTINUOUS_VARS][BINS] = {{0.0}};
    double sum[CONTINUOUS_VARS] = {0.0};
    double sum2[CONTINUOUS_VARS] = {0.0};
    double sum_xy[PAIRS] = {0.0};

    for (; ind < ind_last; ind++) {
        const double *const continuous_vars[CONTINUOUS_VARS] = {
            &ind->w,          &ind->qBDefault,   &ind->qBSeen,        &ind->ChooseGrain, &ind->Choose_ltGrain,
            &ind->MimicGrain, &ind->ImimicGrain, &ind->Imimic_ltGrain};

        // Continous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Bins
            count[variable][select_bin(BIN_SIZE, *continuous_vars[variable])]++;

            // Mean and standard deviation
            sum[variable] += *continuous_vars[variable];
            sum2[variable] += *continuous_vars[variable] * *continuous_vars[variable];
        }

        // Correlations
        sum_xy[CORR_Q_B_SEEN_CHOOSE_GRAIN] += ind->qBSeen * ind->ChooseGrain;
        sum_xy[CORR_Q_B_SEEN_CHOOSE_LT_GRAIN] += ind->qBSeen * ind->Choose_ltGrain;
        sum_xy[CORR_Q_B_SEEN_MIMIC_GRAIN] += ind->qBSeen * ind->MimicGrain;
        sum_xy[CORR_Q_B_SEEN_IMIMIC_GRAIN] += ind->qBSeen * ind->ImimicGrain;
        sum_xy[CORR_Q_B_SEEN_IMIMIC_LT_GRAIN] += ind->qBSeen * ind->Imimic_ltGrain;
        sum_xy[CORR_CHOOSE_GRAIN_CHOOSE_LT_GRAIN] += ind->ChooseGrain * ind->Choose_ltGrain;
        sum_xy[CORR_CHOOSE_GRAIN_MIMIC_GRAIN] += ind->ChooseGrain * ind->MimicGrain;
        sum_xy[CORR_CHOOSE_GRAIN_IMIMIC_GRAIN] += ind->ChooseGrain * ind->ImimicGrain;
        sum_xy[CORR_CHOOSE_GRAIN_IMIMIC_LT_GRAIN] += ind->ChooseGrain * ind->Imimic_ltGrain;
        sum_xy[CORR_CHOOSE_LT_GRAIN_MIMIC_GRAIN] += ind->Choose_ltGrain * ind->MimicGrain;
        sum_xy[CORR_CHOOSE_LT_GRAIN_IMIMIC_GRAIN] += ind->Choose_ltGrain * ind->ImimicGrain;
        sum_xy[CORR_CHOOSE_LT_GRAIN_IMIMIC_LT_GRAIN] += ind->Choose_ltGrain * ind->Imimic_ltGrain;
        sum_xy[CORR_MIMIC_GRAIN_IMIMIC_GRAIN] += ind->MimicGrain * ind->ImimicGrain;
        sum_xy[CORR_MIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->MimicGrain * ind->Imimic_ltGrain;
        sum_xy[CORR_IMIMIC_GRAIN_IMIMIC_LT_GRAIN] += ind->ImimicGrain * ind->Imimic_ltGrain;
    }

    // Continous variables
    for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
        // Bins
        for (int bin = 0; bin < BINS; bin++) {
            double frc = (double)count[variable][bin] / population_size;
            stats->frc[variable][bin] += frc;
            stats->frc2[variable][bin] += frc * frc;
            freq[variable][bin] = frc;  // For quartiles
        }

        // Quartiles
        int    bin = 0;
        double previousfreq = 0.0;

        double lower_quartile = quartile(freq[variable], BINS, LOWER_QUARTILE, &bin, &previousfreq);
        double median = quartile(freq[variable], BINS, MEDIAN, &bin, &previousfreq);
        double upper_quartile = quartile(freq[variable], BINS, UPPER_QUARTILE, &bin, &previousfreq);
        stats->median[variable] += median;
        stats->median2[variable] += median * median;
        double iqr = upper_quartile - lower_quartile;
        stats->iqr[variable] += iqr;
        stats->iqr2[variable] += iqr * iqr;

        // Mean and standard deviation
        double mean = sum[variable] / population_size;
        stats->mean[variable] += mean;
        stats->mean2[variable] += mean * mean;
        double st_dev = stdev(sum[variable], sum2[variable], population_size);
        stats->sd[variable] += st_dev;
        stats->sd2[variable] += st_dev * st_dev;
    }

    // Correlations
    for (int pair = 0; pair < PAIRS; pair++) {
        int    var_x = correlationPairs[pair][0];
        int    var_y = correlationPairs[pair][1];
        double corr = pearson_r(sum[var_x], sum[var_y], sum_xy[pair], sum2[var_x], sum2[var_y], population_size);
        stats->corr[pair] += corr;
        stats->corr2[pair] += corr * corr;
    }
}
