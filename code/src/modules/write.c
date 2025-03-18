#include <stdio.h>

#include "io.h"
#include "math_tools.h"
#include "stats.h"

const char *headers_continuous[CONTINUOUS_VARS] = {
    "w", "qBDefault", "qBSeen", "ChooseGrain", "Choose_ltGrain", "MimicGrain", "ImimicGrain", "Imimic_ltGrain"};
const char *headers_correlations[PAIRS] = {
    "r_qB_Choose",        "r_qB_Choose_lt",        "r_qB_Mimic",      "r_qB_Imimic",        "r_qB_Imimic_lt",
    "r_Choose_Choose_lt", "r_Choose_Mimic",        "r_Choose_Imimic", "r_Choose_Imimic_lt", "r_Choose_lt_Mimic",
    "r_Choose_lt_Imimic", "r_Choose_lt_Imimic_lt", "r_Mimic_Imimic",  "r_Mimic_Imimic_lt",  "r_Imimic_Imimic_lt"};

int write_csv_headers(char *filename);
int write_frq_headers(char *filename);

int stats_csv(Stats *stats, unsigned int periods, unsigned int runs, char *filename) {
    if (write_csv_headers(filename) < 0) {
        return file_write_error(filename);
    }

    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        return file_write_error(filename);
    }

    Stats *stats_p = stats;
    for (unsigned int period = 0; period < periods; period++, stats_p++) {
        // Globals and time
        fprintf(file, "%f,%f,%f,%lu", stats_p->alpha, stats_p->logES, stats_p->Given, stats_p->time);

        // Continuous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Mean and standard deviation
            stats_p->mean2[variable] = stdev(stats_p->mean[variable], stats_p->mean2[variable], runs);
            stats_p->mean[variable] = stats_p->mean[variable] / runs;
            fprintf(file, ",%f,%f", stats_p->mean[variable], stats_p->mean2[variable]);
            stats_p->sd2[variable] = stdev(stats_p->sd[variable], stats_p->sd2[variable], runs);
            stats_p->sd[variable] = stats_p->sd[variable] / runs;
            fprintf(file, ",%f,%f", stats_p->sd[variable], stats_p->sd2[variable]);
        }

        // Correlations
        for (int pair = 0; pair < PAIRS; pair++) {
            stats_p->corr2[pair] = stdev(stats_p->corr[pair], stats_p->corr2[pair], runs);
            stats_p->corr[pair] = stats_p->corr[pair] / runs;
            fprintf(file, ",%f,%f", stats_p->corr[pair], stats_p->corr2[pair]);
        }

        fprintf(file, "\n");
    }

    fclose(file);

    return 0;
}

int stats_frq(Stats *stats, unsigned int periods, unsigned int runs, char *filename) {
    if (write_frq_headers(filename) < 0) {
        return file_write_error(filename);
    }

    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        return file_write_error(filename);
    }

    Stats *stats_p = stats;
    for (unsigned int period = 0; period < periods; period++, stats_p++) {
        // Globals and time
        fprintf(file, "%f,%f,%f,%lu", stats_p->alpha, stats_p->logES, stats_p->Given, stats_p->time);

        // Continuous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Quartiles
            stats_p->median2[variable] = stdev(stats_p->median[variable], stats_p->median2[variable], runs);
            stats_p->median[variable] = stats_p->median[variable] / runs;
            fprintf(file, ",%f,%f", stats_p->median[variable], stats_p->median2[variable]);
            stats_p->iqr2[variable] = stdev(stats_p->iqr[variable], stats_p->iqr2[variable], runs);
            stats_p->iqr[variable] = stats_p->iqr[variable] / runs;
            fprintf(file, ",%f,%f", stats_p->iqr[variable], stats_p->iqr2[variable]);

            // Bins
            for (int bin = 0; bin < BINS; bin++) {
                stats_p->frc2[variable][bin] = stdev(stats_p->frc[variable][bin], stats_p->frc2[variable][bin], runs);
                stats_p->frc[variable][bin] = stats_p->frc[variable][bin] / runs;
                fprintf(file, ",%f,%f", stats_p->frc[variable][bin], stats_p->frc2[variable][bin]);
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
        return file_write_error(filename);
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
        return file_write_error(filename);
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
