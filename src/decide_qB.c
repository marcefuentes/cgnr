#include <math.h>
#include "sim.h"

double calculate(double focal, double partner, double grain);

void decide_qB(struct itype *i, struct itype *i_last, int imimic)
{
	double partner, grain;

	for (; i < i_last; i++) {
		if (i->age > 0 && i->partner->age > 0) {
			if (i->partner == i->oldpartner) {
				if (imimic == 1 && i->Imimic_ltGrain < i->MimicGrain) {
					partner = i->partner->qBSeen_lt;
					grain = i->Imimic_ltGrain;
				} else {
					partner = i->partner->qBSeen;
					grain = i->MimicGrain;
				}
			} else if (imimic == 1) {
				if (i->Imimic_ltGrain < i->ImimicGrain) {
					partner = i->partner->qBSeen_lt;
					grain = i->Imimic_ltGrain;
				} else {
					partner = i->partner->qBSeen;
					grain = i->ImimicGrain;
				}
			}

			i->qBDecided = calculate(i->qBDefault, partner, grain);
		} else {
			i->qBDecided = i->qBDefault;
		}
	}
}

double calculate(double focal, double partner, double grain)
{
	int block = (partner - focal) / grain;
	double block_near = focal + grain * block;
	double block_far;

	if (block < 0) {
		block_far = fmax(0.0, focal + grain * (block - 1));
	} else if (block > 0) {
		block_far = fmin(1.0, focal + grain * (block + 1));
	}

	if (block != 0) {
		focal = (block_near + block_far) / 2.0;
	}

	return focal;
}
