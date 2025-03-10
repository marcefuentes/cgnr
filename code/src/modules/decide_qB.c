#include <math.h>

#include "individual.h"

double calculate(double focal, double partner, double grain);

void decide_qB(struct Individual *ind, struct Individual *ind_last, int imimic) {
    double grain;
    double partner;

    for (; ind < ind_last; ind++) {
        if (ind->age > 0 && ind->partner->age > 0) {
            if (ind->partner == ind->oldpartner) {
                if (imimic == 1 && ind->Imimic_ltGrain < ind->MimicGrain) {
                    partner = ind->partner->qBSeen_lt;
                    grain = ind->Imimic_ltGrain;
                } else {
                    partner = ind->partner->qBSeen;
                    grain = ind->MimicGrain;
                }
                ind->qBDecided = calculate(ind->qBDefault, partner, grain);
            } else if (imimic == 1) {
                if (ind->Imimic_ltGrain < ind->ImimicGrain) {
                    partner = ind->partner->qBSeen_lt;
                    grain = ind->Imimic_ltGrain;
                } else {
                    partner = ind->partner->qBSeen;
                    grain = ind->ImimicGrain;
                }
                ind->qBDecided = calculate(ind->qBDefault, partner, grain);
            } else {
                ind->qBDecided = ind->qBDefault;
            }
        } else {
            ind->qBDecided = ind->qBDefault;
        }
    }
}

double calculate(double focal, double partner, double grain) {
    int    block = (int)((partner - focal) / grain);
    double block_near = focal + (grain * block);
    double block_far;

    if (block < 0) {
        block_far = fmax(0.0, focal + (grain * (block - 1)));
    } else if (block > 0) {
        block_far = fmin(1.0, focal + (grain * (block + 1)));
    }

    if (block != 0) {
        focal = (block_near + block_far) / 2.0;
    }

    return focal;
}
