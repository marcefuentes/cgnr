#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include "sim.h"

// Global variable
extern gsl_rng *rng;

void shuffle_partners(struct itype *i, struct itype *i_last, int groupsize)
{
	int *c;

	c = calloc(groupsize, sizeof *c);
	if (c == NULL) {
		printf("\nFailed calloc (shuffle_partners)");
		exit(EXIT_FAILURE);
	}

	for (int a = 0; a < groupsize; a++) {
		c[a] = a;
	}

	for (; i < i_last; i += groupsize) {
		gsl_ran_shuffle(rng, c, groupsize, sizeof(int));

		for (int a = 0; a < groupsize; a += 2) {
			(i + c[a])->partner = i + c[a + 1];
			(i + c[a + 1])->partner = i + c[a];
		}
	}

	free(c);
}
