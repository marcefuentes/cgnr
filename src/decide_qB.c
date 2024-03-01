#include <math.h>
#include "sim.h"

double calculate(struct itype *i, double grain);

void decide_qB(struct itype *i, struct itype *i_last, int imimic)
{
	for (; i < i_last; i++)
	{
		i->qBDecided = i->qBDefault;

		if (i->age > 0 && i->partner->age > 0)
		{
			if (i->partner == i->oldpartner)
			{
				i->qBDecided = calculate(i, i->MimicGrain);
			}
			else if (imimic == 1)
			{
				i->qBDecided = calculate(i, i->ImimicGrain);
			}
		}
	}
}

double calculate(struct itype *i, double grain)
{
	double focal = i->qBDefault;
	double partner = i->partner->qBSeen;

	int block = (partner - focal) / grain;

	if (block < 0)
	{
		focal += grain*(block - 0.5);

		if (focal < 0.0)
		{
			focal = 0.0;
		}
	}
	if (block > 0)
	{
		focal += grain*(block + 0.5);

		if (focal > 1.0)
		{
			focal = 1.0;
		}
	}

	return focal;
}

