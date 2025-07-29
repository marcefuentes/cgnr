#include <stdio.h>

#include "io.h"
#include "math_tools.h"
#include "stats.h"

const char *headers_continuous[CONTINUOUS_VARS] = {
    "w", "qBDefault", "qBSeen", "ChooseGrain", "Choose_ltGrain", "MimicGrain", "ImimicGrain", "Imimic_ltGrain"};
const char  headers_global[] = "alpha,logES,Given,Time";
const char *headers_correlations[PAIRS] = {
    "r_qB_Choose",        "r_qB_Choose_lt",        "r_qB_Mimic",      "r_qB_Imimic",        "r_qB_Imimic_lt",
    "r_Choose_Choose_lt", "r_Choose_Mimic",        "r_Choose_Imimic", "r_Choose_Imimic_lt", "r_Choose_lt_Mimic",
    "r_Choose_lt_Imimic", "r_Choose_lt_Imimic_lt", "r_Mimic_Imimic",  "r_Mimic_Imimic_lt",  "r_Imimic_Imimic_lt"};

static int write_csv_headers(char *filename);
static int write_frq_headers(char *filename);

int stats_csv(Stats *stats, unsigned int periods, unsigned int runs, char *filename) {
    if (write_csv_headers(filename) < 0) {
        return file_write_error(filename);
    }

    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        return file_write_error(filename);
    }

    double mean;
    double st_dev;
    for (unsigned int period = 0; period < periods; period++) {
        // Globals and time
        fprintf(file, "%f,%f,%f,%lu", stats[period].alpha, stats[period].logES, stats[period].Given,
                stats[period].time);

        // Continuous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Mean and standard deviation
            mean = stats[period].mean[variable] / runs;
            st_dev = stdev(stats[period].mean[variable], stats[period].mean2[variable], runs);
            fprintf(file, ",%f,%f", mean, st_dev);
            mean = stats[period].sd[variable] / runs;
            st_dev = stdev(stats[period].sd[variable], stats[period].sd2[variable], runs);
            fprintf(file, ",%f,%f", mean, st_dev);
        }

        // Correlations
        for (int pair = 0; pair < PAIRS; pair++) {
            mean = stats[period].corr[pair] / runs;
            st_dev = stdev(stats[period].corr[pair], stats[period].corr2[pair], runs);
            fprintf(file, ",%f,%f", mean, st_dev);
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

    double mean;
    double st_dev;
    for (unsigned int period = 0; period < periods; period++) {
        // Globals and time
        fprintf(file, "%f,%f,%f,%lu", stats[period].alpha, stats[period].logES, stats[period].Given,
                stats[period].time);

        // Continuous variables
        for (int variable = 0; variable < CONTINUOUS_VARS; variable++) {
            // Quartiles
            mean = stats[period].median[variable] / runs;
            st_dev = stdev(stats[period].median[variable], stats[period].median2[variable], runs);
            fprintf(file, ",%f,%f", mean, st_dev);
            mean = stats[period].iqr[variable] / runs;
            st_dev = stdev(stats[period].iqr[variable], stats[period].iqr2[variable], runs);
            fprintf(file, ",%f,%f", mean, st_dev);

            // Bins
            for (int bin = 0; bin < BINS; bin++) {
                mean = stats[period].frc[variable][bin] / runs;
                st_dev = stdev(stats[period].frc[variable][bin], stats[period].frc2[variable][bin], runs);
                fprintf(file, ",%f,%f", mean, st_dev);
            }
        }

        fprintf(file, "\n");
    }

    fclose(file);

    return 0;
}

static int write_csv_headers(char *filename) {
    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        return file_write_error(filename);
    }

    // Globals and time
    fprintf(file, "%s", headers_global);

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

static int write_frq_headers(char *filename) {
    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        return file_write_error(filename);
    }

    // Globals and time
    fprintf(file, "%s", headers_global);

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
