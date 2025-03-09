#include <math.h>

#include "sim.h"

static void accumulate_sums(double value, double *sum, double *sum2);
double      correlation(double x, double y, double xy, double x2, double y2, unsigned int n);
static void mean_sd(double *sum, double *sum2, unsigned int n);
static int  select_bin(double binsize, double value);

static void accumulate_sums(double value, double *sum, double *sum2) {
    *sum += value;
    *sum2 += value * value;
}

double correlation(double x, double y, double xy, double x2, double y2, unsigned int n) {
    double numerator = n * xy - x * y;
    double denominator = sqrt((n * x2 - x * x) * (n * y2 - y * y));
    double r = 0.0;

    if (denominator > 0.0) {
        r = numerator / denominator;
    }

    return r;
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

static int select_bin(double binsize, double value) {
    double ceiling = binsize;
    int    bin = 0;

    while (value > ceiling) {
        ceiling += binsize;
        bin++;
    }

    return bin;
}

void stats_end(struct Aggregate *agg, struct Aggregate *agg_last, struct Aggregate *p) {
    for (; agg < agg_last; agg++, p++) {
        p->alpha = agg->alpha;
        p->logES = agg->logES;
        p->Given = agg->Given;
        p->time = agg->time;

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            for (int bin = 0; bin < BINS; bin++) {
                accumulate_sums(agg->frc[variable][bin], &p->frc[variable][bin], &p->frc2[variable][bin]);
            }

            accumulate_sums(agg->median[variable], &p->median[variable], &p->median2[variable]);
            accumulate_sums(agg->iqr[variable], &p->iqr[variable], &p->iqr2[variable]);
            accumulate_sums(agg->mean[variable], &p->mean[variable], &p->mean2[variable]);
            accumulate_sums(agg->sd[variable], &p->sd[variable], &p->sd2[variable]);
        }

        for (int c = 0; c < CORRELATIONS; c++) {
            accumulate_sums(agg->corr[c], &p->corr[c], &p->corr2[c]);
        }
    }
}

void stats_period(struct itype *i, struct itype *i_last, struct Aggregate *agg, unsigned int n) {
    int    count[CONTINUOUS_V][BINS] = {{0}};
    double bins1 = 1.0 / BINS;
    double binsize[CONTINUOUS_V] = {1.0 / BINS, bins1, bins1, bins1, bins1, bins1, bins1, bins1};
    int    correlationPairs[CORRELATIONS][2] = {{2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {3, 4}, {3, 5}, {3, 6},
                                                {3, 7}, {4, 5}, {4, 6}, {4, 7}, {5, 6}, {5, 7}, {6, 7}};

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        agg->mean[variable] = 0.0;
        agg->sd[variable] = 0.0;
    }

    for (int c = 0; c < CORRELATIONS; c++) {
        agg->corr[c] = 0.0;
    }

    for (; i < i_last; i++) {
        double *properties[CONTINUOUS_V] = {&i->w,           &i->qBDefault,      &i->qBSeen,
                                            &i->ChooseGrain, &i->Choose_ltGrain, &i->MimicGrain,
                                            &i->ImimicGrain, &i->Imimic_ltGrain};

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            count[variable][select_bin(binsize[variable], *properties[variable])]++;
            accumulate_sums(*properties[variable], &agg->mean[variable], &agg->sd[variable]);
        }

        agg->corr[0] += i->qBSeen * i->ChooseGrain;
        agg->corr[1] += i->qBSeen * i->Choose_ltGrain;
        agg->corr[2] += i->qBSeen * i->MimicGrain;
        agg->corr[3] += i->qBSeen * i->ImimicGrain;
        agg->corr[4] += i->qBSeen * i->Imimic_ltGrain;
        agg->corr[5] += i->ChooseGrain * i->Choose_ltGrain;
        agg->corr[6] += i->ChooseGrain * i->MimicGrain;
        agg->corr[7] += i->ChooseGrain * i->ImimicGrain;
        agg->corr[8] += i->ChooseGrain * i->Imimic_ltGrain;
        agg->corr[9] += i->Choose_ltGrain * i->MimicGrain;
        agg->corr[10] += i->Choose_ltGrain * i->ImimicGrain;
        agg->corr[11] += i->Choose_ltGrain * i->Imimic_ltGrain;
        agg->corr[12] += i->MimicGrain * i->ImimicGrain;
        agg->corr[13] += i->MimicGrain * i->Imimic_ltGrain;
        agg->corr[14] += i->ImimicGrain * i->Imimic_ltGrain;
    }

    for (int c = 0; c < CORRELATIONS; c++) {
        agg->corr[c] = correlation(agg->mean[correlationPairs[c][0]], agg->mean[correlationPairs[c][1]], agg->corr[c],
                                   agg->sd[correlationPairs[c][0]], agg->sd[correlationPairs[c][1]], n);
    }

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        for (int bin = 0; bin < BINS; bin++) {
            agg->frc[variable][bin] = (double)count[variable][bin] / n;
        }

        int    bin = 0;
        double previousfr = 0.0;
        double fr = agg->frc[variable][bin];

        for (; fr < 0.25; fr += agg->frc[variable][bin]) {
            previousfr = fr;
            bin++;
        }

        double lower_quartile = (double)bin / BINS + (0.25 - previousfr) / ((fr - previousfr) * BINS);

        for (; fr < 0.50; fr += agg->frc[variable][bin]) {
            previousfr = fr;
            bin++;
        }

        agg->median[variable] = (double)bin / BINS + (0.5 - previousfr) / ((fr - previousfr) * BINS);

        for (; fr < 0.75; fr += agg->frc[variable][bin]) {
            previousfr = fr;
            bin++;
        }

        double upper_quartile = (double)bin / BINS + (0.75 - previousfr) / ((fr - previousfr) * BINS);
        agg->iqr[variable] = upper_quartile - lower_quartile;

        mean_sd(&agg->mean[variable], &agg->sd[variable], n);
    }
}

void stats_runs(struct Aggregate *p, struct Aggregate *p_last, unsigned int runs) {
    for (; p < p_last; p++) {
        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            for (int bin = 0; bin < BINS; bin++) {
                mean_sd(&p->frc[variable][bin], &p->frc2[variable][bin], runs);
            }

            mean_sd(&p->median[variable], &p->median2[variable], runs);
            mean_sd(&p->iqr[variable], &p->iqr2[variable], runs);
            mean_sd(&p->mean[variable], &p->mean2[variable], runs);
            mean_sd(&p->sd[variable], &p->sd2[variable], runs);
        }

        for (int c = 0; c < CORRELATIONS; c++) {
            mean_sd(&p->corr[c], &p->corr2[c], runs);
        }
    }
}
