#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "individual.h"
#include "math_tools.h"
#include "stats.h"

const char *headers_continuous[CONTINUOUS_VARS] = {
    "w", "qBDefault", "qBSeen", "ChooseGrain", "Choose_ltGrain", "MimicGrain", "ImimicGrain", "Imimic_ltGrain"};
const char *headers_correlations[PAIRS] = {
    "r_qB_Choose",        "r_qB_Choose_lt",        "r_qB_Mimic",      "r_qB_Imimic",        "r_qB_Imimic_lt",
    "r_Choose_Choose_lt", "r_Choose_Mimic",        "r_Choose_Imimic", "r_Choose_Imimic_lt", "r_Choose_lt_Mimic",
    "r_Choose_lt_Imimic", "r_Choose_lt_Imimic_lt", "r_Mimic_Imimic",  "r_Mimic_Imimic_lt",  "r_Imimic_Imimic_lt"};

void file_write_error(char *filename);
int  write_csv_headers(char *filename);
int  write_frq_headers(char *filename);

int stats_csv(struct Stats *statsall, struct Stats *statsall_last, unsigned int runs, char *filename) {
    if (write_csv_headers(filename) < 0) {
        fprintf(stderr, "Failed write_csv_headers.\n");
        return -1;
    }

    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        file_write_error(filename);
        return -1;
    }

    for (; statsall < statsall_last; statsall++) {
        // Globals and time
        fprintf(file, "%f,%f,%f,%lu", statsall->alpha, statsall->logES, statsall->Given, statsall->time);

        // Continuous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Mean and standard deviation
            statsall->mean2[variable] = stdev(statsall->mean[variable], statsall->mean2[variable], runs);
            statsall->mean[variable] = statsall->mean[variable] / runs;
            fprintf(file, ",%f,%f", statsall->mean[variable], statsall->mean2[variable]);
            statsall->sd2[variable] = stdev(statsall->sd[variable], statsall->sd2[variable], runs);
            statsall->sd[variable] = statsall->sd[variable] / runs;
            fprintf(file, ",%f,%f", statsall->sd[variable], statsall->sd2[variable]);
        }

        // Correlations
        for (int pair = 0; pair < PAIRS; pair++) {
            statsall->corr2[pair] = stdev(statsall->corr[pair], statsall->corr2[pair], runs);
            statsall->corr[pair] = statsall->corr[pair] / runs;
            fprintf(file, ",%f,%f", statsall->corr[pair], statsall->corr2[pair]);
        }

        fprintf(file, "\n");
    }

    fclose(file);

    return 0;
}

int stats_frq(struct Stats *statsall, struct Stats *statsall_last, unsigned int runs, char *filename) {
    if (write_frq_headers(filename) < 0) {
        fprintf(stderr, "Failed write_frq_headers.\n");
        return -1;
    }

    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        file_write_error(filename);
        return -1;
    }

    for (; statsall < statsall_last; statsall++) {
        // Globals and time
        fprintf(file, "%f,%f,%f,%lu", statsall->alpha, statsall->logES, statsall->Given, statsall->time);

        // Continuous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Quartiles
            statsall->median2[variable] = stdev(statsall->median[variable], statsall->median2[variable], runs);
            statsall->median[variable] = statsall->median[variable] / runs;
            fprintf(file, ",%f,%f", statsall->median[variable], statsall->median2[variable]);
            statsall->iqr2[variable] = stdev(statsall->iqr[variable], statsall->iqr2[variable], runs);
            statsall->iqr[variable] = statsall->iqr[variable] / runs;
            fprintf(file, ",%f,%f", statsall->iqr[variable], statsall->iqr2[variable]);

            // Bins
            for (int bin = 0; bin < BINS; bin++) {
                statsall->frc2[variable][bin] =
                    stdev(statsall->frc[variable][bin], statsall->frc2[variable][bin], runs);
                statsall->frc[variable][bin] = statsall->frc[variable][bin] / runs;
                fprintf(file, ",%f,%f", statsall->frc[variable][bin], statsall->frc2[variable][bin]);
            }
        }

        fprintf(file, "\n");
    }

    fclose(file);

    return 0;
}

int write_csv_headers(char *filename) {
    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        file_write_error(filename);
        return -1;
    }

    // Globals and time
    fprintf(file, "alpha,logES,Given,Time");

    // Continuous variables
    for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
        fprintf(file, ",%smean,%smeanSD", headers_continuous[variable], headers_continuous[variable]);
        fprintf(file, ",%ssd,%ssdSD", headers_continuous[variable], headers_continuous[variable]);
    }

    // Correlations
    for (int pair = 0; pair < PAIRS; pair++) {
        fprintf(file, ",%s,%sSD", headers_correlations[pair], headers_correlations[pair]);
    }

    fprintf(file, "\n");
    fclose(file);

    return 0;
}

int write_frq_headers(char *filename) {
    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        file_write_error(filename);
        return -1;
    }

    // Globals and time
    fprintf(file, "alpha,logES,Given,Time");

    // Continuous variables
    for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
        // Quartiles
        fprintf(file, ",%smedian,%smedianSD", headers_continuous[variable], headers_continuous[variable]);
        fprintf(file, ",%siqr,%siqrSD", headers_continuous[variable], headers_continuous[variable]);

        // Bins
        for (int bin = 0; bin < BINS; bin++) {
            fprintf(file, ",%s%i,%s%iSD", headers_continuous[variable], bin, headers_continuous[variable], bin);
        }
    }

    fprintf(file, "\n");
    fclose(file);

    return 0;
}

int write_ics(char *filename, int sequence, float alpha, float logES, float Given, unsigned long time,
              struct Individual *ind, struct Individual *ind_last) {
    char new_filename[18];

    snprintf(new_filename, sizeof(new_filename), "%s_%04d.ics", filename, sequence);

    FILE *file = fopen(new_filename, "a+");
    if (file == NULL) {
        file_write_error(new_filename);
        return -1;
    }

    fprintf(file,
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

    double w_cumulative = 0.0;
    for (; ind < ind_last; ind++) {
        fprintf(file, "\n%f,%f,%f,%lu,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%i", alpha, logES, Given, time, ind->qBDefault,
                ind->qBDecided, ind->qBSeen, ind->partner->qBSeen, ind->wCumulative - w_cumulative, ind->ChooseGrain,
                ind->Choose_ltGrain, ind->MimicGrain, ind->ImimicGrain, ind->Imimic_ltGrain, ind->cost, ind->age);

        w_cumulative = ind->wCumulative;
    }

    fclose(file);

    return 0;
}

int write_time_elapsed(char *filename, float time_elapsed) {
    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        file_write_error(filename);
        return -1;
    }

    fprintf(file, "TimeElapsed,");

    if (time_elapsed < 10.0) {
        fprintf(file, "%f", time_elapsed);
    } else {
        int minute = 60;
        int hour = minute * 60;
        int day = hour * 24;

        int seconds = (int)time_elapsed;
        int days = seconds / day;
        seconds -= days * day;
        int hours = seconds / hour;
        seconds -= hours * hour;
        int minutes = seconds / minute;
        seconds -= minutes * minute;

        if (days > 0) {
            fprintf(file, "%i-", days);

            if (hours < 10) {
                fprintf(file, "0");
            }
        }

        if (days > 0 || hours > 0) {
            fprintf(file, "%i:", hours);

            if (minutes < 10) {
                fprintf(file, "0");
            }
        }

        if (days > 0 || hours > 0 || minutes > 0) {
            fprintf(file, "%i:", minutes);

            if (seconds < 10) {
                fprintf(file, "0");
            }
        }

        fprintf(file, "%i", seconds);
    }

    fprintf(file, "\n");

    fclose(file);

    return 0;
}

void file_write_error(char *filename) { fprintf(stderr, "Failed to open file %s for writing.\n", filename); }
