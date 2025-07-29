#include "individual.h"

Individual *allocate_individuals(unsigned int population_size) {
    Individual *ind = calloc(population_size, sizeof(*ind));
    if (ind == NULL) {
        fprintf(stderr, "Failed to allocate individuals.\n");
        return NULL;
    }

    for (unsigned int individual = 0; individual < population_size; individual++) {
        ind[individual] = INITIAL_INDIVIDUAL;
    }

    return ind;
}

void initial_pairs(Individual *ind_first, Individual *ind_last) {
    Individual *ind_j = ind_first + 1;
    for (Individual *ind_i = ind_first; ind_i < ind_last; ind_i += 2, ind_j += 2) {
        ind_i->partner = ind_j;
        ind_j->partner = ind_i;
    }
}

void update_scores(Individual *ind_first, Individual *ind_last) {
    for (Individual *ind = ind_first; ind < ind_last; ind++) {
        ind->qBSeenSum += ind->qBSeen;
        ind->qBSeen_lt = ind->qBSeenSum / ind->age;
    }
}
