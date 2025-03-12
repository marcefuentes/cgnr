#include "individual.h"

void update_scores(struct Individual *ind, struct Individual *ind_last) {
    for (; ind < ind_last; ind++) {
        ind->qBSeenSum += ind->qBSeen;
        ind->qBSeen_lt = ind->qBSeenSum / ind->age;
    }
}
