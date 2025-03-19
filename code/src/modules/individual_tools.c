#include "individual.h"

void initial_pairs(Individual *ind_first, Individual *ind_last) {
    Individual *ind_j = ind_first + 1;
    for (Individual *ind_i = ind_first; ind_i < ind_last; ind_i += 2, ind_j += 2) {
        ind_i->partner = ind_j;
        ind_j->partner = ind_i;
    }
}

void initial_pairs2(Individual *ind_first[], Individual *ind_last[]) {
    Individual *ind_j = ind_first[1];
    for (Individual *ind_i = ind_first[0]; ind_i < ind_last[0] && ind_j < ind_last[1]; ind_i++, ind_j++) {
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
