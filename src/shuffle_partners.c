#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <stdio.h>
#include <stdlib.h>

#include "sim.h"

// Global variable
extern gsl_rng *rng;

int shuffle_partners(struct itype *i, struct itype *i_last, unsigned int groupsize) {
    unsigned int *c = calloc(groupsize, sizeof(*c));
    if (c == NULL) {
        fprintf(stderr, "Failed calloc (shuffle_partners).\n");
        return -1;
    }

    for (unsigned int a = 0; a < groupsize; a++) {
        c[a] = a;
    }

    for (; i < i_last; i += groupsize) {
        gsl_ran_shuffle(rng, c, groupsize, sizeof(unsigned int));

        for (unsigned int a = 0; a < groupsize; a += 2) {
            (i + c[a])->partner = i + c[a + 1];
            (i + c[a + 1])->partner = i + c[a];
        }
    }

    free(c);

    return 0;
}
