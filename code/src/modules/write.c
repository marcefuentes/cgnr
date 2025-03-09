#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sim.h"

const char *headersc[CONTINUOUS_V] = {"w",          "qBDefault",   "qBSeen",        "ChooseGrain", "Choose_ltGrain",
                                      "MimicGrain", "ImimicGrain", "Imimic_ltGrain"};

const char *headersr[CORRELATIONS] = {
    "r_qB_Choose",        "r_qB_Choose_lt",        "r_qB_Mimic",      "r_qB_Imimic",        "r_qB_Imimic_lt",
    "r_Choose_Choose_lt", "r_Choose_Mimic",        "r_Choose_Imimic", "r_Choose_Imimic_lt", "r_Choose_lt_Mimic",
    "r_Choose_lt_Imimic", "r_Choose_lt_Imimic_lt", "r_Mimic_Imimic",  "r_Mimic_Imimic_lt",  "r_Imimic_Imimic_lt"};

void file_write_error(char *filename);

int write_headers_csv(char *filename) {
    FILE *fp;

    if ((fp = fopen(filename, "a+")) == NULL) {
        file_write_error(filename);
        return -1;
    }

    fprintf(fp, "alpha,logES,Given,Time");

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        fprintf(fp, ",%smean,%smeanSD", headersc[variable], headersc[variable]);
        fprintf(fp, ",%ssd,%ssdSD", headersc[variable], headersc[variable]);
    }

    for (int correlation = 0; correlation < CORRELATIONS; correlation++) {
        fprintf(fp, ",%s,%sSD", headersr[correlation], headersr[correlation]);
    }

    fprintf(fp, "\n");
    fclose(fp);

    return 0;
}

int write_headers_frq(char *filename) {
    FILE *fp;

    if ((fp = fopen(filename, "a+")) == NULL) {
        file_write_error(filename);
        return -1;
    }

    fprintf(fp, "alpha,logES,Given,Time");

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        fprintf(fp, ",%smedian,%smedianSD", headersc[variable], headersc[variable]);
        fprintf(fp, ",%siqr,%siqrSD", headersc[variable], headersc[variable]);

        for (int bin = 0; bin < BINS; bin++) {
            fprintf(fp, ",%s%i,%s%iSD", headersc[variable], bin, headersc[variable], bin);
        }
    }

    fprintf(fp, "\n");
    fclose(fp);

    return 0;
}

int write_stats_csv(char *filename, struct Aggregate *p, struct Aggregate *p_last) {
    FILE *fp;

    if ((fp = fopen(filename, "a+")) == NULL) {
        file_write_error(filename);
        return -1;
    }

    for (; p < p_last; p++) {
        fprintf(fp, "%f,%f,%f,%lu", p->alpha, p->logES, p->Given, p->time);

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            fprintf(fp, ",%f,%f", p->mean[variable], p->mean2[variable]);
            fprintf(fp, ",%f,%f", p->sd[variable], p->sd2[variable]);
        }

        for (int correlation = 0; correlation < CORRELATIONS; correlation++) {
            fprintf(fp, ",%f,%f", p->corr[correlation], p->corr2[correlation]);
        }

        fprintf(fp, "\n");
    }

    fclose(fp);

    return 0;
}

int write_stats_frq(char *filename, struct Aggregate *p, struct Aggregate *p_last) {
    FILE *fp;

    if ((fp = fopen(filename, "a+")) == NULL) {
        file_write_error(filename);
        return -1;
    }

    for (; p < p_last; p++) {
        fprintf(fp, "%f,%f,%f,%lu", p->alpha, p->logES, p->Given, p->time);

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            fprintf(fp, ",%f,%f", p->median[variable], p->median2[variable]);
            fprintf(fp, ",%f,%f", p->iqr[variable], p->iqr2[variable]);

            for (int bin = 0; bin < BINS; bin++) {
                fprintf(fp, ",%f,%f", p->frc[variable][bin], p->frc2[variable][bin]);
            }
        }

        fprintf(fp, "\n");
    }

    fclose(fp);

    return 0;
}

int write_ics(char *filename, int sequence, float alpha, float logES, float Given, unsigned long t,
              struct Individual *i, struct Individual *i_last) {
    char   new_filename[18];
    double wc = 0.0;
    FILE  *fp;

    snprintf(new_filename, sizeof(new_filename), "%s_%04d.ics", filename, sequence);

    if ((fp = fopen(new_filename, "a+")) == NULL) {
        file_write_error(new_filename);
        return -1;
    }

    fprintf(fp,
            "alpha,"
            "logES,"
            "Given,"
            "Time,"
            "qBDefault,"
            "qBDecided,"
            "qBSeen,"
            "qBSeen_j,"
            "w,"
            "ChooseGrain,"
            "Choose_ltGrain,"
            "MimicGrain,"
            "ImimicGrain,"
            "Imimic_ltGrain,"
            "cost,"
            "age");

    for (; i < i_last; i++) {
        fprintf(fp, "\n%f,%f,%f,%lu,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%i", alpha, logES, Given, t, i->qBDefault,
                i->qBDecided, i->qBSeen, i->partner->qBSeen, i->wCumulative - wc, i->ChooseGrain, i->Choose_ltGrain,
                i->MimicGrain, i->ImimicGrain, i->Imimic_ltGrain, i->cost, i->age);

        wc = i->wCumulative;
    }

    fclose(fp);

    return 0;
}

int write_time_elapsed(char *filename, float time_elapsed) {
    FILE *fp;

    if ((fp = fopen(filename, "a+")) == NULL) {
        file_write_error(filename);
        return -1;
    }

    fprintf(fp, "TimeElapsed,");

    if (time_elapsed < 10.0) {
        fprintf(fp, "%f", time_elapsed);
    } else {
        int minute = 60;
        int hour = minute * 60;
        int day = hour * 24;

        int s = (int)time_elapsed;
        int d = s / day;
        s -= d * day;
        int h = s / hour;
        s -= h * hour;
        int m = s / minute;
        s -= m * minute;

        if (d > 0) {
            fprintf(fp, "%i-", d);

            if (h < 10) {
                fprintf(fp, "0");
            }
        }

        if (d > 0 || h > 0) {
            fprintf(fp, "%i:", h);

            if (m < 10) {
                fprintf(fp, "0");
            }
        }

        if (d > 0 || h > 0 || m > 0) {
            fprintf(fp, "%i:", m);

            if (s < 10) {
                fprintf(fp, "0");
            }
        }

        fprintf(fp, "%i", (int)s);
    }

    fprintf(fp, "\n");

    fclose(fp);

    return 0;
}

void file_write_error(char *filename) { fprintf(stderr, "Failed to open file %s for writing.\n", filename); }
