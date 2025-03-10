#include <limits.h>
#include <math.h>
#include <stdio.h>

#include "aggregate.h"
#include "individual.h"

#define EPSILON 1e-6
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

static void   accumulate_sums(double value, double *sum, double *sum2);
static void   mean_sd(double *sum, double *sum2, unsigned int n);
double        pearson_r(double sum_x, double sum_y, double sum_xy, double sum_x2, double sum_y2, unsigned int n);
static double quartile(struct Aggregate *agg, int variable, double threshold, int *bin, double *previousfreq);
static int    select_bin(double binsize, double value);

static void accumulate_sums(double value, double *sum, double *sum2) {
    *sum += value;
    *sum2 += value * value;
}

static void mean_sd(double *sum, double *sum2, unsigned int n) {
    if (n > 1) {
        double numerator = *sum2 - (*sum * *sum / n);
        double variance = numerator / (n - 1);

        if (variance < 0.0) {
            variance = 0.0;
        }

        *sum2 = sqrt(variance);
    } else {
        *sum2 = 0.0;
    }

    *sum /= n;
}

double pearson_r(double sum_x, double sum_y, double sum_xy, double sum_x2, double sum_y2, unsigned int n) {
    double numerator = (n * sum_xy) - (sum_x * sum_y);
    double denominator = sqrt(((n * sum_x2) - (sum_x * sum_x)) * ((n * sum_y2) - (sum_y * sum_y)));
    double pearson_r = 0.0;

    if (denominator > 0.0) {
        pearson_r = numerator / denominator;
    }

    return pearson_r;
}

double quartile(struct Aggregate *agg, int variable, double threshold, int *bin, double *previousfreq) {
    double cumulativeFreq = *previousfreq;
    double freq = 0.0;

    while (cumulativeFreq < threshold) {
        if (*bin >= INT_MAX) {  // Prevent overflow
            fprintf(stderr, "Error: bin overflow in quartile.\n");
            return 0.0;  // Or other error handling
        }
        freq = agg->frc[variable][*bin];
        cumulativeFreq += freq;
        (*bin)++;
    }

    if (cumulativeFreq > threshold) {
        (*bin)--;
        cumulativeFreq -= freq;  // Correct cumulativeFreq
    }

    *previousfreq = cumulativeFreq;  // Update previousfreq
    double delta = agg->frc[variable][*bin];
    if (fabs(delta - 0.0) < EPSILON) {
        // Handle division by zero.
        fprintf(stderr, "Error: Division by zero in quartile.\n");
        return 0.0;
    }

    return ((double)*bin / BINS) + ((threshold - cumulativeFreq) / (delta * BINS));
}

static int select_bin(double binsize, double value) {
    double ceiling = binsize;
    int    bin = 0;

    while (value > ceiling) {
        ceiling += binsize;
        bin++;
    }

    return bin;
}

void stats_end(struct Aggregate *agg, struct Aggregate *agg_last, struct Aggregate *aggall) {
    for (; agg < agg_last; agg++, aggall++) {
        aggall->alpha = agg->alpha;
        aggall->logES = agg->logES;
        aggall->Given = agg->Given;
        aggall->time = agg->time;

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            for (int bin = 0; bin < BINS; bin++) {
                accumulate_sums(agg->frc[variable][bin], &aggall->frc[variable][bin], &aggall->frc2[variable][bin]);
            }

            accumulate_sums(agg->median[variable], &aggall->median[variable], &aggall->median2[variable]);
            accumulate_sums(agg->iqr[variable], &aggall->iqr[variable], &aggall->iqr2[variable]);
            accumulate_sums(agg->mean[variable], &aggall->mean[variable], &aggall->mean2[variable]);
            accumulate_sums(agg->sd[variable], &aggall->sd[variable], &aggall->sd2[variable]);
        }

        for (int pair = 0; pair < PAIRS; pair++) {
            accumulate_sums(agg->corr[pair], &aggall->corr[pair], &aggall->corr2[pair]);
        }
    }
}

void stats_period(struct Individual *ind, struct Individual *ind_last, struct Aggregate *agg, unsigned int n) {
    int    count[CONTINUOUS_V][BINS] = {{0}};
    double binsize[CONTINUOUS_V] = {1.0 / BINS, 1.0 / BINS, 1.0 / BINS, 1.0 / BINS,
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
            count[variable][select_bin(binsize[variable], *properties[variable])]++;
            accumulate_sums(*properties[variable], &agg->mean[variable], &agg->sd[variable]);
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
                      agg->sd[correlationPairs[pair][0]], agg->sd[correlationPairs[pair][1]], n);
    }

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        for (int bin = 0; bin < BINS; bin++) {
            agg->frc[variable][bin] = (double)count[variable][bin] / n;
        }

        int    bin = 0;
        double previousfreq = 0.0;

        double lower_quartile = quartile(agg, variable, LOWER_QUARTILE, &bin, &previousfreq);
        double median = quartile(agg, variable, MEDIAN, &bin, &previousfreq);
        double upper_quartile = quartile(agg, variable, UPPER_QUARTILE, &bin, &previousfreq);

        agg->median[variable] = median;
        agg->iqr[variable] = upper_quartile - lower_quartile;

        mean_sd(&agg->mean[variable], &agg->sd[variable], n);
    }
}

void stats_runs(struct Aggregate *aggall, struct Aggregate *aggall_last, unsigned int runs) {
    for (; aggall < aggall_last; aggall++) {
        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            for (int bin = 0; bin < BINS; bin++) {
                mean_sd(&aggall->frc[variable][bin], &aggall->frc2[variable][bin], runs);
            }

            mean_sd(&aggall->median[variable], &aggall->median2[variable], runs);
            mean_sd(&aggall->iqr[variable], &aggall->iqr2[variable], runs);
            mean_sd(&aggall->mean[variable], &aggall->mean2[variable], runs);
            mean_sd(&aggall->sd[variable], &aggall->sd2[variable], runs);
        }

        for (int pair = 0; pair < PAIRS; pair++) {
            mean_sd(&aggall->corr[pair], &aggall->corr2[pair], runs);
        }
    }
}
