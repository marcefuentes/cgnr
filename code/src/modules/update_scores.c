#include "individual.h"

void update_scores(Individual *ind, Individual *ind_last) {
    for (; ind < ind_last; ind++) {
        ind->qBSeenSum += ind->qBSeen;
        ind->qBSeen_lt = ind->qBSeenSum / ind->age;
    }
}
