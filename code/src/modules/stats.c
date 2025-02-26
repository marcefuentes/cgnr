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

void stats_end(struct pruntype *prun, struct pruntype *prun_last, struct ptype *p) {
    for (; prun < prun_last; prun++, p++) {
        p->alpha = prun->alpha;
        p->logES = prun->logES;
        p->Given = prun->Given;
        p->time = prun->time;

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            for (int bin = 0; bin < BINS; bin++) {
                accumulate_sums(prun->frc[variable][bin], &p->frc[variable][bin], &p->frc2[variable][bin]);
            }

            accumulate_sums(prun->median[variable], &p->median[variable], &p->median2[variable]);
            accumulate_sums(prun->iqr[variable], &p->iqr[variable], &p->iqr2[variable]);
            accumulate_sums(prun->mean[variable], &p->mean[variable], &p->mean2[variable]);
            accumulate_sums(prun->sd[variable], &p->sd[variable], &p->sd2[variable]);
        }

        for (int c = 0; c < CORRELATIONS; c++) {
            accumulate_sums(prun->corr[c], &p->corr[c], &p->corr2[c]);
        }
    }
}

void stats_period(struct itype *i, struct itype *i_last, struct pruntype *prun, unsigned int n) {
    int    count[CONTINUOUS_V][BINS] = {{0}};
    double bins1 = 1.0 / BINS;
    double binsize[CONTINUOUS_V] = {1.0 / BINS, bins1, bins1, bins1, bins1, bins1, bins1, bins1};
    int    correlationPairs[CORRELATIONS][2] = {{2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {3, 4}, {3, 5}, {3, 6},
                                                {3, 7}, {4, 5}, {4, 6}, {4, 7}, {5, 6}, {5, 7}, {6, 7}};

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        prun->mean[variable] = 0.0;
        prun->sd[variable] = 0.0;
    }

    for (int c = 0; c < CORRELATIONS; c++) {
        prun->corr[c] = 0.0;
    }

    for (; i < i_last; i++) {
        double *properties[CONTINUOUS_V] = {&i->w,           &i->qBDefault,      &i->qBSeen,
                                            &i->ChooseGrain, &i->Choose_ltGrain, &i->MimicGrain,
                                            &i->ImimicGrain, &i->Imimic_ltGrain};

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            count[variable][select_bin(binsize[variable], *properties[variable])]++;
            accumulate_sums(*properties[variable], &prun->mean[variable], &prun->sd[variable]);
        }

        prun->corr[0] += i->qBSeen * i->ChooseGrain;
        prun->corr[1] += i->qBSeen * i->Choose_ltGrain;
        prun->corr[2] += i->qBSeen * i->MimicGrain;
        prun->corr[3] += i->qBSeen * i->ImimicGrain;
        prun->corr[4] += i->qBSeen * i->Imimic_ltGrain;
        prun->corr[5] += i->ChooseGrain * i->Choose_ltGrain;
        prun->corr[6] += i->ChooseGrain * i->MimicGrain;
        prun->corr[7] += i->ChooseGrain * i->ImimicGrain;
        prun->corr[8] += i->ChooseGrain * i->Imimic_ltGrain;
        prun->corr[9] += i->Choose_ltGrain * i->MimicGrain;
        prun->corr[10] += i->Choose_ltGrain * i->ImimicGrain;
        prun->corr[11] += i->Choose_ltGrain * i->Imimic_ltGrain;
        prun->corr[12] += i->MimicGrain * i->ImimicGrain;
        prun->corr[13] += i->MimicGrain * i->Imimic_ltGrain;
        prun->corr[14] += i->ImimicGrain * i->Imimic_ltGrain;
    }

    for (int c = 0; c < CORRELATIONS; c++) {
        prun->corr[c] =
            correlation(prun->mean[correlationPairs[c][0]], prun->mean[correlationPairs[c][1]], prun->corr[c],
                        prun->sd[correlationPairs[c][0]], prun->sd[correlationPairs[c][1]], n);
    }

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        for (int bin = 0; bin < BINS; bin++) {
            prun->frc[variable][bin] = (double)count[variable][bin] / n;
        }

        int    bin = 0;
        double previousfr = 0.0;
        double fr = prun->frc[variable][bin];

        for (; fr < 0.25; fr += prun->frc[variable][bin]) {
            previousfr = fr;
            bin++;
        }

        double lower_quartile = (double)bin / BINS + (0.25 - previousfr) / ((fr - previousfr) * BINS);

        for (; fr < 0.50; fr += prun->frc[variable][bin]) {
            previousfr = fr;
            bin++;
        }

        prun->median[variable] = (double)bin / BINS + (0.5 - previousfr) / ((fr - previousfr) * BINS);

        for (; fr < 0.75; fr += prun->frc[variable][bin]) {
            previousfr = fr;
            bin++;
        }

        double upper_quartile = (double)bin / BINS + (0.75 - previousfr) / ((fr - previousfr) * BINS);
        prun->iqr[variable] = upper_quartile - lower_quartile;

        mean_sd(&prun->mean[variable], &prun->sd[variable], n);
    }
}

void stats_runs(struct ptype *p, struct ptype *p_last, unsigned int runs) {
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
