#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <stdio.h>
#include <stdlib.h>

#include "sim.h"

// Global variable
extern gsl_rng *rng;

int shuffle_partners(struct Individual *i, struct Individual *i_last, unsigned int groupsize) {
    unsigned int *random = calloc(groupsize, sizeof(*random));
    if (random == NULL) {
        fprintf(stderr, "Failed calloc (shuffle_partners).\n");
        return -1;
    }

    for (unsigned int individual = 0; individual < groupsize; individual++) {
        random[individual] = individual;
    }

    for (; i < i_last; i += groupsize) {
        gsl_ran_shuffle(rng, random, groupsize, sizeof(unsigned int));

        for (unsigned int individual = 0; individual < groupsize; individual += 2) {
            (i + random[individual])->partner = i + random[individual + 1];
            (i + random[individual + 1])->partner = i + random[individual];
        }
    }

    free(random);

    return 0;
}
