#include <math.h>

#include "individual.h"
#include "math_tools.h"

double fitness(Individual *ind_first, Individual *ind_last, double given, double alpha, double rho) {
    double w_cumulative = 0.0;

    for (Individual *ind = ind_first; ind < ind_last; ind++) {
        double q_A = 1.0 - ind->qBDecided;
        double q_B = (ind->qBDecided * (1.0 - given)) + (ind->partner->qBDecided * given);
        ind->w = fmax(0.0, ces(q_A, q_B, alpha, rho) - ind->cost);
        w_cumulative += ind->w;
        ind->wCumulative = w_cumulative;
        ind->age++;
        ind->qBSeen = ind->qBDecided;
        ind->oldpartner = ind->partner;
    }

    return w_cumulative;
}
