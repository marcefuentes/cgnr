#include <gsl/gsl_randist.h>
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
#include "recruit.h"
#include "stats.h"

/* Simulates reciprocity and partner choice.
 *
 * Create file x.glo with global constants and factors.
 * Run the program with argument x (e.g. 1 if file is 1.glo). */

// Global variables

gsl_rng *rng = NULL;  // Random number generator

// Functions

double fitness(struct Individual *ind, struct Individual *ind_last);
int    simulation(struct Stats *statsall_first, char *filename);
void   start_population(struct Individual *ind, struct Individual *ind_last);

int main(int argc, char *argv[]) {
    clock_t       start = clock();
    int           ret = EXIT_FAILURE;
    struct Stats *statsall_first = NULL;
    char          ics[MAX_FILENAME_LEN];

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

    statsall_first = calloc(globals.periods + 1, sizeof(*statsall_first));
    if (statsall_first == NULL) {
        fprintf(stderr, "Failed calloc (stats).\n");
        goto cleanup;
    }

    struct Stats *statsall_last = statsall_first + globals.periods + 1;

    snprintf(ics, sizeof(ics), "%s.ics", filename);

    for (unsigned int run = 0; run < globals.runs; run++) {
        if (simulation(statsall_first, ics) < 0) {
            fprintf(stderr, "Failed simulation.\n");
            goto cleanup;
        }
    }

    char csv[MAX_FILENAME_LEN];
    snprintf(csv, sizeof(csv), "%s.csv", filename);
    if (stats_csv(statsall_first, statsall_last, globals.runs, csv) < 0) {
        fprintf(stderr, "Failed stats_csv.\n");
        goto cleanup;
    }

    char frq[MAX_FILENAME_LEN];
    snprintf(frq, sizeof(frq), "%s.frq", filename);
    if (stats_frq(statsall_first, statsall_last, globals.runs, frq) < 0) {
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
    if (statsall_first != NULL) {
        free(statsall_first);
        statsall_first = NULL;
    }
    return ret;
}

int simulation(struct Stats *statsall_first, char *filename) {
    int                ret = -1;
    int                sequence = 0;
    struct Individual *ind_first = NULL;
    struct Stats      *stats_first = NULL;

    ind_first = calloc(globals.population_size, sizeof(*ind_first));
    if (ind_first == NULL) {
        fprintf(stderr, "Failed calloc (individuals).\n");
        goto cleanup;
    }

    struct Individual *ind_last = ind_first + globals.population_size;

    stats_first = calloc(globals.periods + 1, sizeof(*stats_first));
    if (stats_first == NULL) {
        fprintf(stderr, "Failed calloc (periods).\n");
        goto cleanup;
    }

    struct Stats *stats_last = stats_first + globals.periods + 1;
    struct Stats *stats = stats_first;

    start_population(ind_first, ind_last);

    for (unsigned long time = 0; time < globals.time; time++) {
        double w_cumulative = fitness(ind_first, ind_last);

        if (time == 0 || (time + 1) % globals.time_per_period == 0) {
            stats->alpha = globals.alpha;
            stats->logES = globals.loges;
            stats->Given = globals.given;
            stats->time = time + 1;
            stats_period(ind_first, ind_last, stats, globals.population_size);
            stats++;
            if (globals.runs == 1) {
                write_ics(filename, sequence, (float)globals.alpha, (float)globals.loges, (float)globals.given,
                          time + 1, ind_first, ind_last);
                sequence++;
            }
        }

        if (globals.language == 1) {
            update_scores(ind_first, ind_last);
        }

        if (globals.shuffle == 1) {
            int shuffle_result = -1;
            shuffle_result = shuffle_partners(ind_first, ind_last, globals.group_size);
            if (shuffle_result < 0) {
                fprintf(stderr, "Failed shuffle_partners.\n");
                goto cleanup;
            }
        }

        if (globals.partner_choice == 1) {
            int choose_partner_result = -1;
            choose_partner_result = choose_partner(ind_first, ind_last, globals.group_size);
            if (choose_partner_result < 0) {
                fprintf(stderr, "Failed choose_partner.\n");
                goto cleanup;
            }
        }

        unsigned int deaths = gsl_ran_binomial(rng, globals.death_rate, globals.population_size);

        if (deaths > 0) {
            struct Recruit *recruit_first = create_recruits(deaths, w_cumulative);
            if (recruit_first == NULL) {
                fprintf(stderr, "Failed create_recruits.\n");
                goto cleanup;
            }
            mutate(ind_first, recruit_first, globals.qb_mutation_size, globals.grain_mutation_size, globals.cost,
                   globals.language);
            kill(recruit_first, ind_first, globals.population_size);
            free_recruit_list(&recruit_first);
        }

        if (globals.reciprocity == 1) {
            decide_qB(ind_first, ind_last, globals.indirect_r);
        }
    }

    stats_end_of_simulation(stats_first, stats_last, statsall_first);
    ret = 0;

cleanup:
    if (ind_first != NULL) {
        free(ind_first);
        ind_first = NULL;
    }
    if (stats_first != NULL) {
        free(stats_first);
        stats_first = NULL;
    }

    return ret;
}

void start_population(struct Individual *ind, struct Individual *ind_last) {
    ind->qBDefault = 0.1;
    ind->qBDecided = ind->qBDefault;
    ind->qBSeenSum = 0.0;
    ind->ChooseGrain = 1.0;
    ind->Choose_ltGrain = 1.0;
    ind->MimicGrain = 1.0;
    ind->ImimicGrain = 1.0;
    ind->Imimic_ltGrain = 1.0;
    ind->cost = 0.0;
    ind->age = 0;

    for (struct Individual *ind_i = ind + 1; ind_i < ind_last; ind_i++) {
        *ind_i = *ind;
    }

    for (struct Individual *ind_j = ind + 1; ind < ind_last; ind += 2, ind_j += 2) {
        ind->partner = ind_j;
        ind_j->partner = ind;
    }
}

double fitness(struct Individual *ind, struct Individual *ind_last) {
    double w_cumulative = 0.0;

    for (; ind < ind_last; ind++) {
        double qA = 1.0 - ind->qBDecided;
        double qB = (ind->qBDecided * (1.0 - globals.given)) + (ind->partner->qBDecided * globals.given);
        ind->w = fmax(0.0, ces(qA, qB, globals.alpha, globals.rho) - ind->cost);
        w_cumulative += ind->w;
        ind->wCumulative = w_cumulative;
        ind->age++;
        ind->qBSeen = ind->qBDecided;
        ind->oldpartner = ind->partner;
    }

    return w_cumulative;
}
