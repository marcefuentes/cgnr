#include <math.h>

#include "fitness.h"

double ces(double qA, double qB, double alpha, double rho) {
    double fitness;

    if (rho > -0.001 && rho < 0.001) {
        fitness = pow(qA, 1.0 - alpha) * pow(qB, alpha);  // Cobb-Douglas
    } else {
        fitness = pow(((1.0 - alpha) * pow(qA, rho)) + (alpha * pow(qB, rho)), 1.0 / rho);
    }

    return fitness;
}
