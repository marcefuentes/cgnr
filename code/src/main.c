#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "individual.h"
#include "io.h"
#include "read.h"
#include "stats.h"

/* Simulates reciprocity and partner choice.
 *
 * Create file x.glo with global constants and factors.
 * Run the program with argument x (e.g. 1 if file is 1.glo). */

// Functions

static int analyze(Stats *stats, char *filename, Individual *ind_first, Individual *ind_last, unsigned long time,
                   unsigned int period, Globals *globals);
static int simulation(Stats *stats, char *filename, Globals *globals);
static int time_to_analyze(unsigned long time, unsigned long time_per_period);

int main(int argc, char *argv[]) {
    clock_t start = clock();
    int     ret = EXIT_FAILURE;
    Stats  *stats = NULL;
    char    ics[MAX_FILENAME_LEN];

    // Check arguments and read global constants

    if (argc != 2) {
        fprintf(stderr, "You must run the program with an argument.\n");
        return EXIT_FAILURE;
    }

    if (strlen(argv[1]) > MAX_ARG_LENGTH) {
        fprintf(stderr, "The argument must have fewer than %d characters.\n", MAX_ARG_LENGTH);
        return EXIT_FAILURE;
    }

    const char *filename = argv[1];

    char glo[MAX_FILENAME_LEN];
    snprintf(glo, sizeof(glo), "%s.glo", filename);
    Globals globals;
    if (read_globals(glo, &globals) < 0) {
        fprintf(stderr, "Failed read_globals.\n");
        goto cleanup;
    }

    // Allocate memory

    stats = calloc(globals.periods, sizeof(*stats));
    if (stats == NULL) {
        fprintf(stderr, "Failed calloc (stats).\n");
        goto cleanup;
    }

    // Run the simulation

    snprintf(ics, sizeof(ics), "%s.ics", filename);

    for (unsigned int run = 0; run < globals.runs; run++) {
        if (simulation(stats, ics, &globals) < 0) {
            fprintf(stderr, "Failed simulation.\n");
            goto cleanup;
        }
    }

    // Write the results

    char csv[MAX_FILENAME_LEN];
    snprintf(csv, sizeof(csv), "%s.csv", filename);
    if (stats_csv(stats, globals.periods, globals.runs, csv) < 0) {
        fprintf(stderr, "Failed stats_csv.\n");
        goto cleanup;
    }

    char frq[MAX_FILENAME_LEN];
    snprintf(frq, sizeof(frq), "%s.frq", filename);
    if (stats_frq(stats, globals.periods, globals.runs, frq) < 0) {
        fprintf(stderr, "Failed stats_frq.\n");
        goto cleanup;
    }

    // End

    if (write_time_elapsed(glo, (float)(clock() - start) / CLOCKS_PER_SEC) < 0) {
        fprintf(stderr, "Failed write_time_elapsed.\n");
        goto cleanup;
    }

    ret = EXIT_SUCCESS;

cleanup:
    if (globals.rng != NULL) {
        gsl_rng_free(globals.rng);
        globals.rng = NULL;
    }
    if (stats != NULL) {
        free(stats);
        stats = NULL;
    }
    return ret;
}

static int simulation(Stats *stats, char *filename, Globals *globals) {
    int ret = -1;

    Individual *ind_first = allocate_individuals(globals->population_size);
    if (ind_first == NULL) {
        fprintf(stderr, "Failed calloc (individuals).\n");
        goto cleanup;
    }

    Individual *ind_last = ind_first + globals->population_size;

    initial_pairs(ind_first, ind_last);

    unsigned int period = 0;

    for (unsigned long time = 0; time < globals->time; time++) {
        double w_cumulative = fitness(ind_first, ind_last, globals->given, globals->alpha, globals->rho);

        if (time_to_analyze(time, globals->time_per_period) == 1) {
            int result = analyze(stats, filename, ind_first, ind_last, time, period, globals);
            if (result < 0) {
                fprintf(stderr, "Failed analyze.\n");
                goto cleanup;
            }
            period++;
        }

        if (globals->language == 1) {
            update_scores(ind_first, ind_last);
        }

        if (globals->shuffle == 1 && shuffle_partners(ind_first, ind_last, globals->group_size, globals->rng) < 0) {
            fprintf(stderr, "Failed shuffle_partners.\n");
            goto cleanup;
        }

        if (globals->partner_choice == 1 &&
            choose_partner(ind_first, ind_last, globals->group_size, globals->rng) < 0) {
            fprintf(stderr, "Failed choose_partner.\n");
            goto cleanup;
        }

        if (handle_recruitment(ind_first, ind_last, w_cumulative, globals) < 0) {
            fprintf(stderr, "Failed handle_recruitment.\n");
            goto cleanup;
        }

        if (globals->reciprocity == 1) {
            decide_qB(ind_first, ind_last, globals->indirect_r);
        }
    }

    ret = 0;

cleanup:
    if (ind_first != NULL) {
        free(ind_first);
        ind_first = NULL;
    }

    return ret;
}

static int analyze(Stats *stats, char *filename, Individual *ind_first, Individual *ind_last, unsigned long time,
                   unsigned int period, Globals *globals) {
    stats[period].alpha = globals->alpha;
    stats[period].logES = globals->loges;
    stats[period].Given = globals->given;
    stats[period].time = time + 1;
    stats_period(ind_first, ind_last, &stats[period], globals->population_size);
    if (globals->runs == 1 && write_ics(filename, period, (float)globals->alpha, (float)globals->loges,
                                        (float)globals->given, time + 1, ind_first, ind_last) < 0) {
        fprintf(stderr, "Failed write_ics.\n");
        return -1;
    }

    return 0;
}

static int time_to_analyze(unsigned long time, unsigned long time_per_period) {
    if (time == 0 || (time + 1) % time_per_period == 0) {
        return 1;
    }
    return 0;
}
