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

gsl_rng *rng;  // Random number generator

// Functions

double fitness(struct Individual *ind, struct Individual *ind_last);
int    simulation(struct Stats *statsall_first, char *filename);
void   start_population(struct Individual *ind, struct Individual *ind_last);

int main(int argc, char *argv[]) {
    clock_t start = clock();

    if (argc != 2) {
        fprintf(stderr, "You must run the program with an argument.\n");
        exit(EXIT_FAILURE);
    }

    if (strlen(argv[1]) > 9) {
        fprintf(stderr, "The argument must have fewer than 9 characters.\n");
        exit(EXIT_FAILURE);
    }

    const char *filename = argv[1];

    char glo[MAX_FILENAME_LEN];
    snprintf(glo, sizeof(glo), "%s.glo", filename);
    if (read_globals(glo) < 0) {
        fprintf(stderr, "Failed read_globals.\n");
        exit(EXIT_FAILURE);
    }

    rng = gsl_rng_alloc(gsl_rng_taus);
    if (rng == NULL) {
        fprintf(stderr, "Failed gsl_rng_alloc.\n");
        exit(EXIT_FAILURE);
    }

    if (globals.seed == 1) {
        struct timeval tval;
        gettimeofday(&tval, 0);
        gsl_rng_set(rng, (unsigned long)(tval.tv_sec) + (unsigned long)(tval.tv_usec));
    }

    struct Stats *statsall_first = calloc(globals.periods + 1, sizeof(*statsall_first));
    if (statsall_first == NULL) {
        fprintf(stderr, "Failed calloc (stats).\n");
        gsl_rng_free(rng);
        exit(EXIT_FAILURE);
    }

    struct Stats *statsall_last = statsall_first + globals.periods + 1;

    char ics[MAX_FILENAME_LEN];
    snprintf(ics, sizeof(ics), "%s.ics", filename);

    for (unsigned int run = 0; run < globals.runs; run++) {
        if (simulation(statsall_first, ics) < 0) {
            fprintf(stderr, "Failed simulation.\n");
            gsl_rng_free(rng);
            free(statsall_first);
            exit(EXIT_FAILURE);
        }
    }

    char csv[MAX_FILENAME_LEN];
    snprintf(csv, sizeof(csv), "%s.csv", filename);
    if (stats_csv(statsall_first, statsall_last, globals.runs, csv) < 0) {
        fprintf(stderr, "Failed stats_csv.\n");
        gsl_rng_free(rng);
        free(statsall_first);
        exit(EXIT_FAILURE);
    }

    char frq[MAX_FILENAME_LEN];
    snprintf(frq, sizeof(frq), "%s.frq", filename);
    if (stats_frq(statsall_first, statsall_last, globals.runs, frq) < 0) {
        fprintf(stderr, "Failed stats_frq.\n");
        gsl_rng_free(rng);
        free(statsall_first);
        exit(EXIT_FAILURE);
    }

    gsl_rng_free(rng);
    free(statsall_first);

    if (write_time_elapsed(glo, (float)(clock() - start) / CLOCKS_PER_SEC) < 0) {
        fprintf(stderr, "Failed write_time_elapsed.\n");
        exit(EXIT_FAILURE);
    }

    return 0;
}

int simulation(struct Stats *statsall_first, char *filename) {
    int sequence = 0;

    struct Individual *ind_first = calloc(globals.population_size, sizeof(*ind_first));
    if (ind_first == NULL) {
        fprintf(stderr, "Failed calloc (individuals).\n");
        return -1;
    }

    struct Individual *ind_last = ind_first + globals.population_size;

    struct Stats *stats_first = calloc(globals.periods + 1, sizeof(*stats_first));
    if (stats_first == NULL) {
        fprintf(stderr, "Failed calloc (periods).\n");
        free(ind_first);
        free(stats_first);
        return -1;
    }

    struct Stats *stats_last = stats_first + globals.periods + 1;
    struct Stats *stats = stats_first;

    start_population(ind_first, ind_last);

    for (unsigned long time = 0; time < globals.time; time++) {
        double w_cumulative = fitness(ind_first, ind_last);

        if (time == 0 || (time + 1) % (globals.time / globals.periods) == 0) {
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
            if (shuffle_partners(ind_first, ind_last, globals.group_size) < 0) {
                fprintf(stderr, "Failed shuffle_partners.\n");
                free(ind_first);
                free(stats_first);
                return -1;
            }
        }

        if (globals.partner_choice == 1) {
            if (choose_partner(ind_first, ind_last, globals.group_size) < 0) {
                fprintf(stderr, "Failed choose_partner.\n");
                free(ind_first);
                free(stats_first);
                return -1;
            }
        }

        unsigned int deaths = gsl_ran_binomial(rng, globals.death_rate, globals.population_size);

        if (deaths > 0) {
            struct Recruit *recruit_first = create_recruits(deaths, w_cumulative);
            if (recruit_first == NULL) {
                fprintf(stderr, "Failed create_recruits.\n");
                free(ind_first);
                free(stats_first);
                return -1;
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
    free(ind_first);
    free(stats_first);

    return 0;
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

    for (struct Individual *ind_j = ind + 1; ind_j < ind_last; ind_j++) {
        *ind_j = *ind;
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
