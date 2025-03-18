#include "individual.h"

void update_scores(Individual *ind_first, Individual *ind_last) {
    for (Individual *ind = ind_first; ind < ind_last; ind++) {
        ind->qBSeenSum += ind->qBSeen;
        ind->qBSeen_lt = ind->qBSeenSum / ind->age;
    }
}
