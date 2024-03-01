#include <stdio.h>
#include <stdlib.h>
#include "sim.h"
 
const char* headersc[CONTINUOUS_V] = { "w",
				       "qBDefault",
				       "qBSeen",
				       "ChooseGrain",
				       "Choose_ltGrain",
				       "MimicGrain",
				       "ImimicGrain",
				       "Imimic_ltGrain" };

const char* headersr[CORRELATIONS] = { "r_qB_Choose",
				       "r_qB_Choose_lt",
				       "r_qB_Mimic",
				       "r_qB_Imimic",
				       "r_qB_Imimic_lt",
				       "r_Choose_Choose_lt",
				       "r_Choose_Mimic",
				       "r_Choose_Imimic",
				       "r_Choose_Imimic_lt",
				       "r_Choose_lt_Mimic",
				       "r_Choose_lt_Imimic",
				       "r_Choose_lt_Imimic_lt",
				       "r_Mimic_Imimic",
				       "r_Mimic_Imimic_lt",
				       "r_Imimic_Imimic_lt" };

void write_headers_csv(char *filename)
{
	FILE *fp;

	if ((fp = fopen(filename, "a+")) == NULL)
	{
		file_write_error(filename);
	}

	fprintf(fp, "alpha,logES,Given,Time");

	for (int v = 0; v < CONTINUOUS_V; v++)
	{
		fprintf(fp, ",%smean,%smeanSD", headersc[v], headersc[v]);
		fprintf(fp, ",%ssd,%ssdSD", headersc[v], headersc[v]);
	}

	for (int c = 0; c < CORRELATIONS; c++)
	{
		fprintf(fp, ",%s,%sSD", headersr[c], headersr[c]);
	}

	fprintf(fp, "\n");

	fclose(fp);
}

void write_headers_frq(char *filename)
{
	FILE *fp;

	if ((fp = fopen(filename, "a+")) == NULL)
	{
		file_write_error(filename);
	}

	fprintf(fp, "alpha,logES,Given,Time");

	for (int v = 0; v < CONTINUOUS_V; v++)
	{
		fprintf(fp, ",%smedian,%smedianSD", headersc[v], headersc[v]);
		fprintf(fp, ",%siqr,%siqrSD", headersc[v], headersc[v]);

		for (int b = 0; b < BINS; b++)
		{
			fprintf(fp, ",%s%i,%s%iSD", headersc[v], b, headersc[v], b);
		}
	}

	fprintf(fp, "\n");

	fclose(fp);
}

void write_stats_csv(char *filename, struct ptype *p, struct ptype *p_last)
{
	FILE *fp;

	if ((fp = fopen(filename, "a+")) == NULL)
	{
		file_write_error(filename);
	}

	for (; p < p_last; p++)
	{
		fprintf(fp, "%f,%f,%f,%i", p->alpha, p->logES, p->Given, p->time);

		for (int v = 0; v < CONTINUOUS_V; v++)
		{
			fprintf(fp, ",%f,%f", p->mean[v], p->mean2[v]);
			fprintf(fp, ",%f,%f", p->sd[v], p->sd2[v]);
		}

		for (int c = 0; c < CORRELATIONS; c++)
		{
			fprintf(fp, ",%f,%f", p->corr[c], p->corr2[c]);
		}

		fprintf(fp, "\n");
	}

	fclose(fp);
}

void write_stats_frq(char *filename, struct ptype *p, struct ptype *p_last)
{
	FILE *fp;

	if ((fp = fopen(filename, "a+")) == NULL)
	{
		file_write_error(filename);
	}

	for (; p < p_last; p++)
	{
		fprintf(fp, "%f,%f,%f,%i", p->alpha, p->logES, p->Given, p->time);

		for (int v = 0; v < CONTINUOUS_V; v++)
		{
			fprintf(fp, ",%f,%f", p->median[v], p->median2[v]);
			fprintf(fp, ",%f,%f", p->iqr[v], p->iqr2[v]);

			for (int b = 0; b < BINS; b++)
			{
				fprintf(fp, ",%f,%f", p->c[v][b], p->c2[v][b]);
			}
		}

		fprintf(fp, "\n");
	}

	fclose(fp);
}

void write_headers_i(char *filename)
{
	FILE *fp;

	if ((fp = fopen(filename, "a+")) == NULL)
	{
		file_write_error(filename);
	}

	fprintf(fp,
		    "alpha,"
		    "logES,"
		    "Given,"
		    "qBDefault,"
		    "qBDecided,"
		    "qBSeen,"
		    "qBSeenSum,"
		    "w,"
		    "ChooseGrain,"
		    "Choose_ltGrain,"
		    "MimicGrain,"
		    "ImimicGrain,"
		    "Imimic_ltGrain,"
		    "cost,"
		    "age");

	fclose(fp);
}

void write_i(char *filename, float alpha, float logES, float Given, struct itype *i, struct itype *i_last)
{
	double wc = 0.0;
	FILE *fp;

	if ((fp = fopen(filename, "a+")) == NULL)
	{
		file_write_error(filename);
	}

	for (; i < i_last; i++)
	{
		fprintf(fp, "\n%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%i",
			     alpha,
			     logES,
			     Given,
			     i->qBDefault,
			     i->qBDecided,
			     i->qBSeen,
			     i->qBSeenSum,
			     i->wCumulative - wc,
			     i->ChooseGrain,
			     i->Choose_ltGrain,
			     i->MimicGrain,
			     i->ImimicGrain,
			     i->Imimic_ltGrain,
			     i->cost,
			     i->age);

		wc = i->wCumulative;
	}

	fclose(fp);
}


void write_time_elapsed(char *filename, float time_elapsed)
{
	FILE *fp;

	if ((fp = fopen(filename, "a+")) == NULL)
	{
		file_write_error(filename);
	}

	fprintf(fp, "TimeElapsed,");

	if (time_elapsed < 10.0)
	{
		fprintf(fp, "%f", time_elapsed);
	}
	else
	{
		int minute = 60;
		int hour = minute*60;
		int day = hour*24;

		int s = time_elapsed;
		int d = s/day;
		s -= d*day;
		int h = s/hour;
		s -= h*hour;
		int m = s/minute;
		s -= m*minute;

		if (d > 0)
		{
			fprintf(fp, "%i-", d);

			if (h < 10)
			{
				fprintf(fp, "0");
			}
		}

		if (d > 0 || h > 0)
		{
			fprintf(fp, "%i:", h);

			if (m < 10)
			{
				fprintf(fp, "0");
			}
		}
		
		if (d > 0 || h > 0 || m > 0)
		{
			fprintf(fp, "%i:", m);

			if (s < 10)
			{
				fprintf(fp, "0");
			}
		}

		fprintf(fp, "%i", (int)s);
	}

	fprintf(fp, "\n");

	fclose(fp);
}

void file_write_error(char *filename)
{
	fprintf(stderr, "Can't open file %s to write.\n", filename);
	exit(EXIT_FAILURE);
}
