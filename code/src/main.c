#include <gsl/gsl_rng.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>

#include "globals.h"
#include "individual.h"
#include "io.h"
#include "math_tools.h"
#include "stats.h"

/* Simulates reciprocity and partner choice.
 *
 * Create file x.glo with global constants and factors.
 * Run the program with argument x (e.g. 1 if file is 1.glo). */

// Global variables

gsl_rng *rng = NULL;  // Random number generator

// Functions

static Individual *allocate_individuals(unsigned int population_size);
static int    analyze(Stats *stats, char *filename, Individual *ind_first, Individual *ind_last, unsigned long time,
                      unsigned int period);
static double fitness(Individual *ind_first, Individual *ind_last);
static void   initial_pairs(Individual *ind_first, Individual *ind_last);
static int    simulation(Stats *stats, char *filename);
static int    time_to_analyze(unsigned long time);

int main(int argc, char *argv[]) {
    clock_t start = clock();
    int     ret = EXIT_FAILURE;
    Stats  *stats = NULL;
    char    ics[MAX_FILENAME_LEN];

    if (argc != 2) {
        fprintf(stderr, "You must run the program with an argument.\n");
        goto cleanup;
    }

    if (strlen(argv[1]) > MAX_ARG_LENGTH) {
        fprintf(stderr, "The argument must have fewer than %d characters.\n", MAX_ARG_LENGTH);
        goto cleanup;
    }

    const char *filename = argv[1];

    char glo[MAX_FILENAME_LEN];
    snprintf(glo, sizeof(glo), "%s.glo", filename);
    if (read_globals(glo) < 0) {
        fprintf(stderr, "Failed read_globals.\n");
        goto cleanup;
    }

    rng = gsl_rng_alloc(gsl_rng_taus);
    if (rng == NULL) {
        fprintf(stderr, "Failed gsl_rng_alloc.\n");
        goto cleanup;
    }

    if (globals.seed == 1) {
        struct timeval tval;
        gettimeofday(&tval, 0);
        gsl_rng_set(rng, (unsigned long)(tval.tv_sec) + (unsigned long)(tval.tv_usec));
    }

    stats = calloc(globals.periods + 1, sizeof(*stats));
    if (stats == NULL) {
        fprintf(stderr, "Failed calloc (stats).\n");
        goto cleanup;
    }

    snprintf(ics, sizeof(ics), "%s.ics", filename);

    for (unsigned int run = 0; run < globals.runs; run++) {
        if (simulation(stats, ics) < 0) {
            fprintf(stderr, "Failed simulation.\n");
            goto cleanup;
        }
    }

    char csv[MAX_FILENAME_LEN];
    snprintf(csv, sizeof(csv), "%s.csv", filename);
    if (stats_csv(stats, globals.periods + 1, globals.runs, csv) < 0) {
        fprintf(stderr, "Failed stats_csv.\n");
        goto cleanup;
    }

    char frq[MAX_FILENAME_LEN];
    snprintf(frq, sizeof(frq), "%s.frq", filename);
    if (stats_frq(stats, globals.periods + 1, globals.runs, frq) < 0) {
        fprintf(stderr, "Failed stats_frq.\n");
        goto cleanup;
    }

    if (write_time_elapsed(glo, (float)(clock() - start) / CLOCKS_PER_SEC) < 0) {
        fprintf(stderr, "Failed write_time_elapsed.\n");
        goto cleanup;
    }

    ret = EXIT_SUCCESS;

cleanup:
    if (rng != NULL) {
        gsl_rng_free(rng);
        rng = NULL;
    }
    if (stats != NULL) {
        free(stats);
        stats = NULL;
    }
    return ret;
}

static int simulation(Stats *stats, char *filename) {
    int ret = -1;

    Individual *ind_first = allocate_individuals(globals.population_size);
    if (ind_first == NULL) {
        fprintf(stderr, "Failed calloc (individuals).\n");
        goto cleanup;
    }

    Individual *ind_last = ind_first + globals.population_size;

    initial_pairs(ind_first, ind_last);

    unsigned int period = 0;

    for (unsigned long time = 0; time < globals.time; time++) {
        double w_cumulative = fitness(ind_first, ind_last);

        if (time_to_analyze(time) == 1) {
            int result = analyze(stats, filename, ind_first, ind_last, time, period);
            if (result < 0) {
                fprintf(stderr, "Failed analyze.\n");
                goto cleanup;
            }
            period++;
        }

        if (globals.language == 1) {
            update_scores(ind_first, ind_last);
        }

        if (globals.shuffle == 1 && shuffle_partners(ind_first, ind_last, globals.group_size) < 0) {
            fprintf(stderr, "Failed shuffle_partners.\n");
            goto cleanup;
        }

        if (globals.partner_choice == 1 && choose_partner(ind_first, ind_last, globals.group_size) < 0) {
            fprintf(stderr, "Failed choose_partner.\n");
            goto cleanup;
        }

        if (handle_recruitment(ind_first, ind_last, w_cumulative, globals.death_rate, globals.qb_mutation_size,
                               globals.grain_mutation_size, globals.cost, globals.language,
                               globals.population_size) < 0) {
            fprintf(stderr, "Failed handle_recruitment.\n");
            goto cleanup;
        }

        if (globals.reciprocity == 1) {
            decide_qB(ind_first, ind_last, globals.indirect_r);
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

static Individual *allocate_individuals(unsigned int population_size) {
    Individual *ind = calloc(population_size, sizeof(*ind));
    if (ind == NULL) {
        fprintf(stderr, "Failed to allocate individuals.\n");
        return NULL;
    }

    ind[0] = INITIAL_INDIVIDUAL;

    for (unsigned int individual = 1; individual < population_size; individual++) {
        ind[individual] = ind[0];
    }

    return ind;
}

static int analyze(Stats *stats, char *filename, Individual *ind_first, Individual *ind_last, unsigned long time,
                   unsigned int period) {
    stats[period].alpha = globals.alpha;
    stats[period].logES = globals.loges;
    stats[period].Given = globals.given;
    stats[period].time = time + 1;
    stats_period(ind_first, ind_last, &stats[period], globals.population_size);
    if (globals.runs == 1) {
        if (write_ics(filename, period, (float)globals.alpha, (float)globals.loges, (float)globals.given, time + 1,
                      ind_first, ind_last) < 0) {
            fprintf(stderr, "Failed write_ics.\n");
            return -1;
        }
    }

    return 0;
}

static double fitness(Individual *ind_first, Individual *ind_last) {
    double w_cumulative = 0.0;

    for (Individual *ind = ind_first; ind < ind_last; ind++) {
        double q_A = 1.0 - ind->qBDecided;
        double q_B = (ind->qBDecided * (1.0 - globals.given)) + (ind->partner->qBDecided * globals.given);
        ind->w = fmax(0.0, ces(q_A, q_B, globals.alpha, globals.rho) - ind->cost);
        w_cumulative += ind->w;
        ind->wCumulative = w_cumulative;
        ind->age++;
        ind->qBSeen = ind->qBDecided;
        ind->oldpartner = ind->partner;
    }

    return w_cumulative;
}

static void initial_pairs(Individual *ind_first, Individual *ind_last) {
    Individual *ind_j = ind_first + 1;
    for (Individual *ind_i = ind_first; ind_i < ind_last; ind_i += 2, ind_j += 2) {
        ind_i->partner = ind_j;
        ind_j->partner = ind_i;
    }
}

static int time_to_analyze(unsigned long time) {
    if (time == 0 || (time + 1) % globals.time_per_period == 0) {
        return 1;
    }
    return 0;
}
