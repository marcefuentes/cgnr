#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <stdio.h>
#include <stdlib.h>

#include "individual.h"

int shuffle_partners(Individual *ind_first, Individual *ind_last, unsigned int group_size, gsl_rng *rng) {
    unsigned int *random = calloc(group_size, sizeof(*random));
    if (random == NULL) {
        fprintf(stderr, "Failed calloc (shuffle_partners).\n");
        return -1;
    }

    for (unsigned int individual = 0; individual < group_size; individual++) {
        random[individual] = individual;
    }

    for (Individual *ind = ind_first; ind < ind_last; ind += group_size) {
        gsl_ran_shuffle(rng, random, group_size, sizeof(unsigned int));

        for (unsigned int individual = 0; individual < group_size; individual += 2) {
            (ind + random[individual])->partner = ind + random[individual + 1];
            (ind + random[individual + 1])->partner = ind + random[individual];
        }
    }

    free(random);

    return 0;
}
