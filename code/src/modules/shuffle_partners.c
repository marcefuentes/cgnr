#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <stdio.h>
#include <stdlib.h>

#include "individual.h"

// Global variable
extern gsl_rng *rng;

int shuffle_partners(struct Individual *ind, struct Individual *ind_last, unsigned int groupsize) {
    unsigned int *random = calloc(groupsize, sizeof(*random));
    if (random == NULL) {
        fprintf(stderr, "Failed calloc (shuffle_partners).\n");
        return -1;
    }

    for (unsigned int individual = 0; individual < groupsize; individual++) {
        random[individual] = individual;
    }

    for (; ind < ind_last; ind += groupsize) {
        gsl_ran_shuffle(rng, random, groupsize, sizeof(unsigned int));

        for (unsigned int individual = 0; individual < groupsize; individual += 2) {
            (ind + random[individual])->partner = ind + random[individual + 1];
            (ind + random[individual + 1])->partner = ind + random[individual];
        }
    }

    free(random);

    return 0;
}
