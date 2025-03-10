#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sim.h"

const char *headersc[CONTINUOUS_V] = {"w",          "qBDefault",   "qBSeen",        "ChooseGrain", "Choose_ltGrain",
                                      "MimicGrain", "ImimicGrain", "Imimic_ltGrain"};

const char *headersr[PAIRS] = {
    "r_qB_Choose",        "r_qB_Choose_lt",        "r_qB_Mimic",      "r_qB_Imimic",        "r_qB_Imimic_lt",
    "r_Choose_Choose_lt", "r_Choose_Mimic",        "r_Choose_Imimic", "r_Choose_Imimic_lt", "r_Choose_lt_Mimic",
    "r_Choose_lt_Imimic", "r_Choose_lt_Imimic_lt", "r_Mimic_Imimic",  "r_Mimic_Imimic_lt",  "r_Imimic_Imimic_lt"};

void file_write_error(char *filename);

int write_headers_csv(char *filename) {
    FILE *file_pointer = fopen(filename, "a+");
    if (file_pointer == NULL) {
        file_write_error(filename);
        return -1;
    }

    fprintf(file_pointer, "alpha,logES,Given,Time");

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        fprintf(file_pointer, ",%smean,%smeanSD", headersc[variable], headersc[variable]);
        fprintf(file_pointer, ",%ssd,%ssdSD", headersc[variable], headersc[variable]);
    }

    for (int pair = 0; pair < PAIRS; pair++) {
        fprintf(file_pointer, ",%s,%sSD", headersr[pair], headersr[pair]);
    }

    fprintf(file_pointer, "\n");
    fclose(file_pointer);

    return 0;
}

int write_headers_frq(char *filename) {
    FILE *file_pointer = fopen(filename, "a+");
    if (file_pointer == NULL) {
        file_write_error(filename);
        return -1;
    }

    fprintf(file_pointer, "alpha,logES,Given,Time");

    for (int variable = 0; variable < CONTINUOUS_V; variable++) {
        fprintf(file_pointer, ",%smedian,%smedianSD", headersc[variable], headersc[variable]);
        fprintf(file_pointer, ",%siqr,%siqrSD", headersc[variable], headersc[variable]);

        for (int bin = 0; bin < BINS; bin++) {
            fprintf(file_pointer, ",%s%i,%s%iSD", headersc[variable], bin, headersc[variable], bin);
        }
    }

    fprintf(file_pointer, "\n");
    fclose(file_pointer);

    return 0;
}

int write_stats_csv(char *filename, struct Aggregate *aggall, struct Aggregate *aggall_last) {
    FILE *file_pointer = fopen(filename, "a+");
    if (file_pointer == NULL) {
        file_write_error(filename);
        return -1;
    }

    for (; aggall < aggall_last; aggall++) {
        fprintf(file_pointer, "%f,%f,%f,%lu", aggall->alpha, aggall->logES, aggall->Given, aggall->time);

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            fprintf(file_pointer, ",%f,%f", aggall->mean[variable], aggall->mean2[variable]);
            fprintf(file_pointer, ",%f,%f", aggall->sd[variable], aggall->sd2[variable]);
        }

        for (int pair = 0; pair < PAIRS; pair++) {
            fprintf(file_pointer, ",%f,%f", aggall->corr[pair], aggall->corr2[pair]);
        }

        fprintf(file_pointer, "\n");
    }

    fclose(file_pointer);

    return 0;
}

int write_stats_frq(char *filename, struct Aggregate *aggall, struct Aggregate *aggall_last) {
    FILE *file_pointer = fopen(filename, "a+");
    if (file_pointer == NULL) {
        file_write_error(filename);
        return -1;
    }

    for (; aggall < aggall_last; aggall++) {
        fprintf(file_pointer, "%f,%f,%f,%lu", aggall->alpha, aggall->logES, aggall->Given, aggall->time);

        for (int variable = 0; variable < CONTINUOUS_V; variable++) {
            fprintf(file_pointer, ",%f,%f", aggall->median[variable], aggall->median2[variable]);
            fprintf(file_pointer, ",%f,%f", aggall->iqr[variable], aggall->iqr2[variable]);

            for (int bin = 0; bin < BINS; bin++) {
                fprintf(file_pointer, ",%f,%f", aggall->frc[variable][bin], aggall->frc2[variable][bin]);
            }
        }

        fprintf(file_pointer, "\n");
    }

    fclose(file_pointer);

    return 0;
}

int write_ics(char *filename, int sequence, float alpha, float logES, float Given, unsigned long time,
              struct Individual *ind, struct Individual *ind_last) {
    char new_filename[18];

    snprintf(new_filename, sizeof(new_filename), "%s_%04d.ics", filename, sequence);

    FILE *file_pointer = fopen(new_filename, "a+");
    if (file_pointer == NULL) {
        file_write_error(new_filename);
        return -1;
    }

    fprintf(file_pointer,
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

    double wcumulative = 0.0;
    for (; ind < ind_last; ind++) {
        fprintf(file_pointer, "\n%f,%f,%f,%lu,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%i", alpha, logES, Given, time,
                ind->qBDefault, ind->qBDecided, ind->qBSeen, ind->partner->qBSeen, ind->wCumulative - wcumulative,
                ind->ChooseGrain, ind->Choose_ltGrain, ind->MimicGrain, ind->ImimicGrain, ind->Imimic_ltGrain,
                ind->cost, ind->age);

        wcumulative = ind->wCumulative;
    }

    fclose(file_pointer);

    return 0;
}

int write_time_elapsed(char *filename, float time_elapsed) {
    FILE *file_pointer = fopen(filename, "a+");
    if (file_pointer == NULL) {
        file_write_error(filename);
        return -1;
    }

    fprintf(file_pointer, "TimeElapsed,");

    if (time_elapsed < 10.0) {
        fprintf(file_pointer, "%f", time_elapsed);
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
            fprintf(file_pointer, "%i-", days);

            if (hours < 10) {
                fprintf(file_pointer, "0");
            }
        }

        if (days > 0 || hours > 0) {
            fprintf(file_pointer, "%i:", hours);

            if (minutes < 10) {
                fprintf(file_pointer, "0");
            }
        }

        if (days > 0 || hours > 0 || minutes > 0) {
            fprintf(file_pointer, "%i:", minutes);

            if (seconds < 10) {
                fprintf(file_pointer, "0");
            }
        }

        fprintf(file_pointer, "%i", seconds);
    }

    fprintf(file_pointer, "\n");

    fclose(file_pointer);

    return 0;
}

void file_write_error(char *filename) { fprintf(stderr, "Failed to open file %s for writing.\n", filename); }
