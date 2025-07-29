#include <stdio.h>
#include <sys/time.h>

#include "globals.h"

int initialize_rng(Globals *globals) {
    globals->rng = gsl_rng_alloc(gsl_rng_taus);
    if (globals->rng == NULL) {
        fprintf(stderr, "Failed gsl_rng_alloc.\n");
        return -1;
    }

    if (globals->seed == 1) {
        struct timeval tval;
        gettimeofday(&tval, 0);
        gsl_rng_set(globals->rng, (unsigned long)(tval.tv_sec) + (unsigned long)(tval.tv_usec));
    } else {
        gsl_rng_set(globals->rng, (unsigned long)globals->seed);
    }

    return 0;
}
