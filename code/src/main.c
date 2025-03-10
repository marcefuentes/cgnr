#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>

#include "dtnorm.h"  // From https://github.com/alanrogers/dtnorm
#include "sim.h"

#define READ_KEY(file_pointer, key, var, type)                  \
    if (read_key_value(file_pointer, key, &(var), #type) < 0) { \
        fclose(file_pointer);                                   \
        return -1;                                              \
    }

/* Simulates reciprocity and partner choice.
 *
 * Create file x.glo with global constants and factors.
 * Run the program with argument x (e.g. 1 if file is 1.glo). */

// Global variable needed in other files

gsl_rng *rng;  // Random number generator

// Global variables needed in this file

int           gSeed;  // Seed random numbers
unsigned int  gN;     // Population size
unsigned int  gRuns;
unsigned long gTime;
unsigned int  gPeriods;            // Periods recorded
double        gqBMutationSize;     // For qBDefault
double        gGrainMutationSize;  // For ChooseGrain and MimicGrain
double        gDeathRate;
unsigned int  gGroupSize;  // Number of individuals that an individual can watch (including itself)
double        gCost;
int           gPartnerChoice;
int           gReciprocity;
int           gIndirectR;
int           gLanguage;  // Individuals access lifelong behavior of partners
int           gShuffle;   // Shuffle partners in markets every time step
double        gGiven;
double        galpha;
double        glogES, grho;  // Elasticity of substitution. ES = 1/(1 - rho)
                             // CES fitness function: w = (alpha*qA^rho + (1 - alpha)*qB^rho)^(1/rho)

// Functions

int    caso(struct Aggregate *aggall_first, char *filename);
double ces(double qA, double qB);  // glogES, galpha
double fitness(struct Individual *ind, struct Individual *ind_last);
int    read_globals(char *filename);
void   start_population(struct Individual *ind, struct Individual *ind_last);
void   update_scores(struct Individual *ind, struct Individual *ind_last);

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

    char csv[MAX_FILENAME_LEN];
    char frq[MAX_FILENAME_LEN];
    char ics[MAX_FILENAME_LEN];

    snprintf(csv, sizeof(csv), "%s.csv", filename);
    snprintf(frq, sizeof(frq), "%s.frq", filename);
    snprintf(ics, sizeof(ics), "%s.ics", filename);

    if (write_headers_csv(csv) < 0) {
        fprintf(stderr, "Failed write_headers_csv.\n");
        exit(EXIT_FAILURE);
    }
    if (write_headers_frq(frq) < 0) {
        fprintf(stderr, "Failed write_headers_frq.\n");
        exit(EXIT_FAILURE);
    }

    rng = gsl_rng_alloc(gsl_rng_taus);
    if (rng == NULL) {
        fprintf(stderr, "Failed gsl_rng_alloc.\n");
        exit(EXIT_FAILURE);
    }

    if (gSeed == 1) {
        struct timeval tval;
        gettimeofday(&tval, 0);
        gsl_rng_set(rng, (unsigned long)(tval.tv_sec) + (unsigned long)(tval.tv_usec));
    }

    struct Aggregate *aggall_first = calloc(gPeriods + 1, sizeof(*aggall_first));
    if (aggall_first == NULL) {
        fprintf(stderr, "Failed calloc (periods).\n");
        gsl_rng_free(rng);
        exit(EXIT_FAILURE);
    }

    struct Aggregate *aggall_last = aggall_first + gPeriods + 1;

    if (caso(aggall_first, ics) < 0) {
        fprintf(stderr, "Failed caso.\n");
        gsl_rng_free(rng);
        free(aggall_first);
        exit(EXIT_FAILURE);
    }

    stats_runs(aggall_first, aggall_last, gRuns);
    if (write_stats_csv(csv, aggall_first, aggall_last) < 0) {
        fprintf(stderr, "Failed write_stats_csv.\n");
        gsl_rng_free(rng);
        free(aggall_first);
        exit(EXIT_FAILURE);
    }
    if (write_stats_frq(frq, aggall_first, aggall_last) < 0) {
        fprintf(stderr, "Failed write_stats_frq.\n");
        gsl_rng_free(rng);
        free(aggall_first);
        exit(EXIT_FAILURE);
    }

    gsl_rng_free(rng);
    free(aggall_first);

    if (write_time_elapsed(glo, (float)(clock() - start) / CLOCKS_PER_SEC) < 0) {
        fprintf(stderr, "Failed write_time_elapsed.\n");
        exit(EXIT_FAILURE);
    }

    return 0;
}

int read_globals(char *filename) {
    FILE *file_pointer = fopen(filename, "r");
    if (file_pointer == NULL) {
        fprintf(stderr, "Failed to open file %s for reading.\n", filename);
        return -1;
    }

    READ_KEY(file_pointer, "Seed", gSeed, int);
    READ_KEY(file_pointer, "N", gN, unsigned int);
    READ_KEY(file_pointer, "Runs", gRuns, unsigned int);
    READ_KEY(file_pointer, "Time", gTime, unsigned long);
    READ_KEY(file_pointer, "Periods", gPeriods, unsigned int);
    READ_KEY(file_pointer, "qBMutationSize", gqBMutationSize, double);
    READ_KEY(file_pointer, "GrainMutationSize", gGrainMutationSize, double);
    READ_KEY(file_pointer, "DeathRate", gDeathRate, double);
    READ_KEY(file_pointer, "GroupSize", gGroupSize, unsigned int);
    READ_KEY(file_pointer, "Cost", gCost, double);
    READ_KEY(file_pointer, "PartnerChoice", gPartnerChoice, int);
    READ_KEY(file_pointer, "Reciprocity", gReciprocity, int);
    READ_KEY(file_pointer, "IndirectR", gIndirectR, int);
    READ_KEY(file_pointer, "Language", gLanguage, int);
    READ_KEY(file_pointer, "Shuffle", gShuffle, int);
    READ_KEY(file_pointer, "alpha", galpha, double);
    READ_KEY(file_pointer, "logES", glogES, double);
    READ_KEY(file_pointer, "Given", gGiven, double);

    fclose(file_pointer);

    gN = (unsigned int)(pow(2.0, (double)gN) + 0.5);
    gTime = (unsigned long)(pow(2.0, (double)gTime) + 0.5);
    gPeriods = (unsigned int)(pow(2.0, (double)gPeriods) + 0.5);
    gqBMutationSize = pow(2.0, gqBMutationSize);
    gGrainMutationSize = pow(2.0, gGrainMutationSize);
    gDeathRate = pow(2.0, gDeathRate);
    gGroupSize = (unsigned int)(pow(2.0, (double)gGroupSize) + 0.5);
    gCost = pow(2.0, gCost);
    grho = 1.0 - 1.0 / pow(2.0, glogES);

    return 0;
}

int caso(struct Aggregate *aggall_first, char *filename) {
    int sequence = 0;

    for (unsigned int run = 0; run < gRuns; run++) {
        struct Individual *ind_first = calloc(gN, sizeof(*ind_first));
        if (ind_first == NULL) {
            fprintf(stderr, "Failed calloc (individuals).\n");
            return -1;
        }

        struct Individual *ind_last = ind_first + gN;

        struct Aggregate *agg_first = calloc(gPeriods + 1, sizeof(*agg_first));
        if (agg_first == NULL) {
            fprintf(stderr, "Failed calloc (periods of each run).\n");
            free(ind_first);
            free(agg_first);
            return -1;
        }

        struct Aggregate *agg_last = agg_first + gPeriods + 1;
        struct Aggregate *agg = agg_first;

        start_population(ind_first, ind_last);

        for (unsigned long time = 0; time < gTime; time++) {
            double wcumulative = fitness(ind_first, ind_last);

            if (time == 0 || (time + 1) % (gTime / gPeriods) == 0) {
                agg->alpha = galpha;
                agg->logES = glogES;
                agg->Given = gGiven;
                agg->time = time + 1;
                stats_period(ind_first, ind_last, agg, gN);
                agg++;
                if (gRuns == 1) {
                    write_ics(filename, sequence, (float)galpha, (float)glogES, (float)gGiven, time + 1, ind_first,
                              ind_last);
                    sequence++;
                }
            }

            if (gLanguage == 1) {
                update_scores(ind_first, ind_last);
            }

            if (gShuffle == 1) {
                if (shuffle_partners(ind_first, ind_last, gGroupSize) < 0) {
                    fprintf(stderr, "Failed shuffle_partners.\n");
                    free(ind_first);
                    free(agg_first);
                    return -1;
                }
            }

            if (gPartnerChoice == 1) {
                if (choose_partner(ind_first, ind_last, gGroupSize) < 0) {
                    fprintf(stderr, "Failed choose_partner.\n");
                    free(ind_first);
                    free(agg_first);
                    return -1;
                }
            }

            unsigned int deaths = gsl_ran_binomial(rng, gDeathRate, gN);

            if (deaths > 0) {
                struct Recruit *recruit_first = create_recruits(deaths, wcumulative);
                if (recruit_first == NULL) {
                    fprintf(stderr, "Failed create_recruits.\n");
                    free(ind_first);
                    free(agg_first);
                    return -1;
                }
                struct Individual *ind = ind_first;

                for (struct Recruit *recruit = recruit_first; recruit != NULL; recruit = recruit->next) {
                    while (recruit->randomwc > ind->wCumulative) {
                        ind++;
                    }

                    recruit->qBDefault = dtnorm(ind->qBDefault, gqBMutationSize, 0.0, 1.0, rng);
                    recruit->ChooseGrain = dtnorm(ind->ChooseGrain, gGrainMutationSize, 0.0, 1.0, rng);
                    recruit->MimicGrain = dtnorm(ind->MimicGrain, gGrainMutationSize, 0.0, 1.0, rng);
                    recruit->ImimicGrain = dtnorm(ind->ImimicGrain, gGrainMutationSize, 0.0, 1.0, rng);
                    if (gLanguage == 1) {
                        recruit->Choose_ltGrain = dtnorm(ind->Choose_ltGrain, gGrainMutationSize, 0.0, 1.0, rng);
                        recruit->Imimic_ltGrain = dtnorm(ind->Imimic_ltGrain, gGrainMutationSize, 0.0, 1.0, rng);
                    } else {
                        recruit->Choose_ltGrain = ind->Choose_ltGrain;
                        recruit->Imimic_ltGrain = ind->Imimic_ltGrain;
                    }

                    recruit->cost =
                        -gCost * (log(recruit->ChooseGrain) + log(recruit->Choose_ltGrain) + log(recruit->MimicGrain) +
                                  log(recruit->ImimicGrain) + log(recruit->Imimic_ltGrain));
                }

                kill(recruit_first, ind_first, gN);
                free_recruit_list(&recruit_first);
            }

            if (gReciprocity == 1) {
                decide_qB(ind_first, ind_last, gIndirectR);
            }
        }

        stats_end(agg_first, agg_last, aggall_first);
        free(ind_first);
        free(agg_first);
    }

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
    double wcumulative = 0.0;

    for (; ind < ind_last; ind++) {
        double qA = 1.0 - ind->qBDecided;
        double qB = (ind->qBDecided * (1.0 - gGiven)) + (ind->partner->qBDecided * gGiven);
        ind->w = fmax(0.0, ces(qA, qB) - ind->cost);
        wcumulative += ind->w;
        ind->wCumulative = wcumulative;
        ind->age++;
        ind->qBSeen = ind->qBDecided;
        ind->oldpartner = ind->partner;
    }

    return wcumulative;
}

double ces(double qA, double qB) {
    double w;

    if (grho > -0.001 && grho < 0.001) {
        w = pow(qA, 1.0 - galpha) * pow(qB, galpha);  // Cobb-Douglas
    } else {
        w = pow(((1.0 - galpha) * pow(qA, grho)) + (galpha * pow(qB, grho)), 1.0 / grho);
    }

    return w;
}

void update_scores(struct Individual *ind, struct Individual *ind_last) {
    for (; ind < ind_last; ind++) {
        ind->qBSeenSum += ind->qBSeen;
        ind->qBSeen_lt = ind->qBSeenSum / ind->age;
    }
}
