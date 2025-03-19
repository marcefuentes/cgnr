#include "individual.h"

void initial_pairs(Individual *ind_first, Individual *ind_last) {
    Individual *ind_j = ind_first + 1;
    for (Individual *ind_i = ind_first; ind_i < ind_last; ind_i += 2, ind_j += 2) {
        ind_i->partner = ind_j;
        ind_j->partner = ind_i;
    }
}
