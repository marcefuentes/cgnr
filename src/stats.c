#include <math.h>
#include "sim.h"

int select_bin(double binsize, double v);
double stdev(double sum, double sum2, int n);
double correlation(double x, double y, double xy, double x2, double y2, int n);

void stats_period(struct itype *i, struct itype *i_last, struct pruntype *prun, int n)
{
	int bin[CONTINUOUS_V][BINS] = {{ 0 }};
	int correlationPairs[CORRELATIONS][2] = { { 2, 3 },
						  { 2, 4 },
						  { 2, 5 },
						  { 2, 6 },
						  { 2, 7 },
						  { 3, 4 },
						  { 3, 5 },
						  { 3, 6 },
						  { 3, 7 },
						  { 4, 5 },
						  { 4, 6 },
						  { 4, 7 },
						  { 5, 6 },
						  { 5, 7 },
						  { 6, 7 } };
	double binsize = 1.0/BINS;
	double e, f, qi, qs;
	int b;

	for (int v = 0; v < CONTINUOUS_V; v++)
	{
		prun->mean[v] = 0.0;
		prun->sd[v] = 0.0;
	}

	for (int c = 0; c < CORRELATIONS; c++)
	{
		prun->corr[c] = 0.0;
	}

	for (; i < i_last; i++)
	{
		double* properties[CONTINUOUS_V] = { &i->w,
						     &i->qBDefault,
						     &i->qBSeen,
						     &i->ChooseGrain,
						     &i->Choose_ltGrain,
						     &i->MimicGrain,
						     &i->ImimicGrain,
						     &i->Imimic_ltGrain };

		for (int v = 0; v < CONTINUOUS_V; v++)
		{
			bin[v][select_bin(binsize, *properties[v])] ++;
			prun->mean[v] += *properties[v];
			prun->sd[v] += *properties[v] * (*properties[v]);
		}

		prun->corr[0]	+= i->qBSeen		* i->ChooseGrain;
		prun->corr[1]	+= i->qBSeen		* i->Choose_ltGrain;
		prun->corr[2]	+= i->qBSeen		* i->MimicGrain;
		prun->corr[3]	+= i->qBSeen		* i->ImimicGrain;
		prun->corr[4]	+= i->qBSeen		* i->Imimic_ltGrain;
		prun->corr[5]	+= i->ChooseGrain	* i->Choose_ltGrain;
		prun->corr[6]	+= i->ChooseGrain	* i->MimicGrain;
		prun->corr[7]	+= i->ChooseGrain	* i->ImimicGrain;
		prun->corr[8]	+= i->ChooseGrain	* i->Imimic_ltGrain;
		prun->corr[9]	+= i->Choose_ltGrain	* i->MimicGrain;
		prun->corr[10]	+= i->Choose_ltGrain	* i->ImimicGrain;
		prun->corr[11]	+= i->Choose_ltGrain	* i->Imimic_ltGrain;
		prun->corr[12]	+= i->MimicGrain	* i->ImimicGrain;
		prun->corr[13]	+= i->MimicGrain	* i->Imimic_ltGrain;
		prun->corr[14]	+= i->ImimicGrain	* i->Imimic_ltGrain;

	}

	for (int c = 0; c < CORRELATIONS; c++)
	{
		prun->corr[c] = correlation(prun->mean[correlationPairs[c][0]],
					    prun->mean[correlationPairs[c][1]],
					    prun->corr[c],
					    prun->sd[correlationPairs[c][0]],
					    prun->sd[correlationPairs[c][1]],
					    n);
	}

	for (int v = 0; v < CONTINUOUS_V; v++)
	{
		for (b = 0; b < BINS; b++)
		{
			prun->frc[v][b] = (double)bin[v][b] / n;
		}

		b = 0;
		e = 0.0;

		for (f = prun->frc[v][b]; f < 0.25; f += prun->frc[v][b])
		{
			e = f;
			b++;
		}

		qi = (double)b/BINS + (0.25 - e)/((f - e)*BINS);

		for (; f < 0.5; f += prun->frc[v][b])
		{
			e = f;
			b++;
		}

		prun->median[v] = (double)b/BINS + (0.5 - e) / ((f - e)*BINS);

		for (; f < 0.75; f += prun->frc[v][b])
		{
			e = f;
			b++;
		}

		qs = (double)b/BINS + (0.75 - e) / ((f - e)*BINS);
		prun->iqr[v] = qs - qi;

		prun->sd[v] = stdev(prun->mean[v], prun->sd[v], n);
		prun->mean[v] = prun->mean[v]/n;
	}
}

int select_bin(double binsize, double v)
{
	double ceiling = binsize;
	int b = 0;

	while (v > ceiling)
	{
		ceiling += binsize;
		b++;
	}

	return b;
}

void stats_end(struct pruntype *prun, struct pruntype *prun_last, struct ptype *p)
{
	for (; prun < prun_last; prun++, p++)
	{
		p->alpha = prun->alpha;
		p->logES = prun->logES;
		p->Given = prun->Given;
		p->time  = prun->time;

		for (int v = 0; v < CONTINUOUS_V; v++)
		{
			for (int b = 0; b < BINS; b++)
			{
				p->c[v][b]  += prun->frc[v][b];
				p->c2[v][b] += prun->frc[v][b] * prun->frc[v][b];
			}

			p->median[v]	+= prun->median[v];
			p->median2[v]	+= prun->median[v] * prun->median[v];

			p->iqr[v]	+= prun->iqr[v];
			p->iqr2[v]	+= prun->iqr[v] * prun->iqr[v];
			
			p->mean[v]	+= prun->mean[v];
			p->mean2[v]	+= prun->mean[v] * prun->mean[v];

			p->sd[v]	+= prun->sd[v];
			p->sd2[v]	+= prun->sd[v] * prun->sd[v];
		}

		for (int c = 0; c < CORRELATIONS; c++)
		{
			p->corr[c]	+= prun->corr[c];
			p->corr2[c]	+= prun->corr[c] * prun->corr[c];
		}
	}
}

void stats_runs(struct ptype *p, struct ptype *p_last, int runs)
{
	for (; p < p_last; p++)
	{
		for (int v = 0; v < CONTINUOUS_V; v++)
		{
			for (int b = 0; b < BINS; b++)
			{
				p->c2[v][b] = stdev(p->c[v][b], p->c2[v][b], runs);
				p->c[v][b] /= runs;
			}

			p->median2[v]	= stdev(p->median[v], p->median2[v], runs);
			p->median[v]	/= runs;
			p->iqr2[v]	= stdev(p->iqr[v], p->iqr2[v], runs);
			p->iqr[v]	/= runs;
			p->mean2[v]	= stdev(p->mean[v], p->mean2[v], runs);
			p->mean[v]	/= runs;
			p->sd2[v]	= stdev(p->sd[v], p->sd2[v], runs);
			p->sd[v]	/= runs;
		}

		for (int c = 0; c < CORRELATIONS; c++)
		{
			p->corr2[c]	= stdev(p->corr[c], p->corr2[c], runs);
			p->corr[c]	/= runs;
		}
	}
}

double stdev(double sum, double sum2, int n)
{
	double sd;

	// When the standard deviation is zero, small roundoff errors can
	// cause the argument of sqrt to be negative.  This generates NaN.

	if (n > 1)
	{
		sd = sqrt((sum2 - sum*sum/n)/(n - 1));
	}
	else
	{
		sd = 0.0;
	}

	return sd;
}

double correlation(double x, double y, double xy, double x2, double y2, int n)
{
	double r, numerator, denominator;

	numerator = n*xy - x*y;
	denominator = sqrt((n*x2 - x*x) * (n*y2 - y*y));

	if (denominator > 0.0)
	{
		r = numerator/denominator;
	}
	else
	{
		r = 0.0;
	}

	return r;
}
