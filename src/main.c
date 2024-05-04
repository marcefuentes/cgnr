#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include "sim.h"
#include "dtnorm.h" // From https://github.com/alanrogers/dtnorm

/* Simulates reciprocity and partner choice.
 *
 * Create file x.glo with global constants and factors.
 * Run the program with argument x (e.g. 1 if file is 1.glo). */

// Global variable needed in other files

gsl_rng *rng; // Random number generator

// Global variables needed in this file

int gSeed; // Seed random numbers
int gN; // Population size
int gRuns;
int gTime;
int gPeriods; // Periods recorded
double gqBMutationSize; // For qBDefault
double gGrainMutationSize; // For ChooseGrain and MimicGrain
double gDeathRate;
int gGroupSize; // Number of individuals that an individual can watch (including itself)
double gCost;
int gPartnerChoice;
int gReciprocity;
int gIndirectR;
int gLanguage; // Individuals access lifelong behavior of partners
int gShuffle; // Shuffle partners in markets every time step
double gGiven;
double galpha;
double glogES, grho; // Elasticity of substitution. ES = 1/(1 - rho)
	// CES fitness function: w = (alpha*qA^rho + (1 - alpha)*qB^rho)^(1/rho)

// Functions

void read_globals(char *filename);
void caso(struct ptype *p_first, char *filename);
void start_population(struct itype *i, struct itype *i_last);
double fitness(struct itype *i, struct itype *i_last);
double ces(double qA, double qB); // glogES, galpha
void update_scores(struct itype *i, struct itype *i_last);

int main(int argc, char *argv[])
{
	struct ptype *p_first, *p_last;
	clock_t start = clock();

	if (argc != 2) {
		fprintf(stderr, "You must run the program with an argument.\n");
		exit(EXIT_FAILURE);
	} else if (strlen(argv[1]) > 8) {
		fprintf(stderr,
			"The argument must have fewer than 8 characters.\n");
		exit(EXIT_FAILURE);
	}

	char glo[13];
	char csv[13];
	char ics[13];
	char frq[13];
	strcpy(glo, argv[1]);
	strcpy(csv, argv[1]);
	strcpy(ics, argv[1]);
	strcpy(frq, argv[1]);
	strcat(glo, ".glo");
	strcat(csv, ".csv");
	strcat(ics, ".ics");
	strcat(frq, ".frq");

	write_headers_csv(csv);
	write_headers_frq(frq);
	read_globals(glo);
	if (gRuns == 1) {
		write_headers_i(ics);
	}

	rng = gsl_rng_alloc(gsl_rng_taus);

	if (gSeed == 1) {
		struct timeval tv;
		gettimeofday(&tv, 0);
		gsl_rng_set(rng, tv.tv_sec + tv.tv_usec);
	}

	p_first = calloc(gPeriods + 1, sizeof *p_first);
	if (p_first == NULL) {
		printf("\nFailed calloc (periods)");
		exit(EXIT_FAILURE);
	}

	caso(p_first, ics);

	p_last = p_first + gPeriods + 1;
	stats_runs(p_first, p_last, gRuns);
	write_stats_csv(csv, p_first, p_last); // Writes periodic data
	write_stats_frq(frq, p_first, p_last); // Writes periodic data

	free(p_first);

	gsl_rng_free(rng);

	write_time_elapsed(glo, (float)(clock() - start) / CLOCKS_PER_SEC);

	return 0;
}

void read_globals(char *filename)
{
	FILE *fp;

	if ((fp = fopen(filename, "r")) == NULL) {
		fprintf(stderr, "Can't open file %s to read.\n", filename);
		exit(EXIT_FAILURE);
	}

	gSeed = read_int(fp, "Seed,%i\n", &gSeed, "Seed");
	gN = read_int(fp, "N,%i\n", &gN, "N");
	gRuns = read_int(fp, "Runs,%i\n", &gRuns, "Runs");
	gTime = read_int(fp, "Time,%i\n", &gTime, "Time");
	gPeriods = read_int(fp, "Periods,%i\n", &gPeriods, "Periods");
	gqBMutationSize = read_double(fp, "qBMutationSize,%lf\n",
				      &gqBMutationSize, "qBMutationSize");
	gGrainMutationSize = read_double(fp, "GrainMutationSize,%lf\n",
					 &gGrainMutationSize,
					 "GrainMutationSize");
	gDeathRate =
		read_double(fp, "DeathRate,%lf\n", &gDeathRate, "DeathRate");
	gGroupSize = read_int(fp, "GroupSize,%i\n", &gGroupSize, "GroupSize");
	gCost = read_double(fp, "Cost,%lf\n", &gCost, "Cost");
	gPartnerChoice = read_int(fp, "PartnerChoice,%i\n", &gPartnerChoice,
				  "PartnerChoice");
	gReciprocity =
		read_int(fp, "Reciprocity,%i\n", &gReciprocity, "Reciprocity");
	gIndirectR = read_int(fp, "IndirectR,%i\n", &gIndirectR, "IndirectR");
	gLanguage = read_int(fp, "Language,%i\n", &gLanguage, "Language");
	gShuffle = read_int(fp, "Shuffle,%i\n", &gShuffle, "Shuffle");
	galpha = read_double(fp, "alpha,%lf\n", &galpha, "alpha");
	glogES = read_double(fp, "logES,%lf\n", &glogES, "logES");
	gGiven = read_double(fp, "Given,%lf\n", &gGiven, "Given");

	fclose(fp);

	gN = pow(2.0, gN);
	gTime = pow(2.0, gTime);
	gPeriods = pow(2.0, gPeriods);
	gqBMutationSize = pow(2.0, gqBMutationSize);
	gGrainMutationSize = pow(2.0, gGrainMutationSize);
	gDeathRate = pow(2.0, gDeathRate);
	gGroupSize = pow(2.0, gGroupSize);
	gCost = pow(2.0, gCost);
	grho = 1.0 - 1.0 / pow(2.0, glogES);
}

void caso(struct ptype *p_first, char *filename)
{
	struct itype *i_first, *i_last;
	struct pruntype *prun_first, *prun_last, *prun;

	for (int r = 0; r < gRuns; r++) {
		i_first = calloc(gN, sizeof *i_first);
		if (i_first == NULL) {
			printf("\nFailed calloc (individuals)");
			exit(EXIT_FAILURE);
		}

		i_last = i_first + gN;

		prun_first = calloc(gPeriods + 1, sizeof *prun_first);
		if (prun_first == NULL) {
			printf("\nFailed calloc (periods of each run)");
			exit(EXIT_FAILURE);
		}

		prun_last = prun_first + gPeriods + 1;
		prun = prun_first;

		start_population(i_first, i_last);

		for (int t = 0; t < gTime; t++) {
			double wC = fitness(i_first, i_last);

			if (t == 0 || (t + 1) % (gTime / gPeriods) == 0) {
				prun->alpha = galpha;
				prun->logES = glogES;
				prun->Given = gGiven;
				prun->time = t + 1;
				stats_period(i_first, i_last, prun, gN);
				prun++;
				if (gRuns == 1 && t == gTime - 1) {
					write_i(filename, (float)galpha,
						(float)glogES, (float)gGiven,
						i_first, i_last);
				}
			}

			if (gLanguage == 1) {
				update_scores(i_first, i_last);
			}

			if (gShuffle == 1) {
				shuffle_partners(i_first, i_last, gGroupSize);
			}

			if (gPartnerChoice == 1) {
				choose_partner(i_first, i_last, gGroupSize);
			}

			int deaths = gsl_ran_binomial(rng, gDeathRate, gN);

			if (deaths > 0) {
				struct rtype *recruit_first =
					create_recruits(deaths, wC);
				struct itype *i = i_first;

				for (struct rtype *recruit = recruit_first;
				     recruit != NULL; recruit = recruit->next) {
					while (recruit->randomwc >
					       i->wCumulative) {
						i++;
					}

					recruit->qBDefault = dtnorm(
						i->qBDefault, gqBMutationSize,
						0.0, 1.0, rng);
					recruit->ChooseGrain =
						dtnorm(i->ChooseGrain,
						       gGrainMutationSize, 0.0,
						       1.0, rng);
					recruit->MimicGrain =
						dtnorm(i->MimicGrain,
						       gGrainMutationSize, 0.0,
						       1.0, rng);
					recruit->ImimicGrain =
						dtnorm(i->ImimicGrain,
						       gGrainMutationSize, 0.0,
						       1.0, rng);
					if (gLanguage == 1) {
						recruit->Choose_ltGrain = dtnorm(
							i->Choose_ltGrain,
							gGrainMutationSize, 0.0,
							1.0, rng);
						recruit->Imimic_ltGrain = dtnorm(
							i->Imimic_ltGrain,
							gGrainMutationSize, 0.0,
							1.0, rng);
					} else {
						recruit->Choose_ltGrain =
							i->Choose_ltGrain;
						recruit->Imimic_ltGrain =
							i->Imimic_ltGrain;
					}
				}

				kill(recruit_first, i_first, gN, gCost);
				free_recruits(recruit_first);
			}

			if (gReciprocity == 1) {
				decide_qB(i_first, i_last, gIndirectR);
			}
		}

		free(i_first);

		stats_end(prun_first, prun_last, p_first);
		free(prun_first);
	}
}

void start_population(struct itype *i, struct itype *i_last)
{
	struct itype *j;

	i->qBDefault = 0.1;
	i->qBDecided = i->qBDefault;
	i->qBSeenSum = 0.0;
	i->ChooseGrain = 1.0;
	i->Choose_ltGrain = 1.0;
	i->MimicGrain = 1.0;
	i->ImimicGrain = 1.0;
	i->Imimic_ltGrain = 1.0;
	i->cost = 0.0;
	i->age = 0;

	for (j = i + 1; j < i_last; j++) {
		*j = *i;
	}

	for (j = i + 1; i < i_last; i += 2, j += 2) {
		i->partner = j;
		j->partner = i;
	}
}

double fitness(struct itype *i, struct itype *i_last)
{
	double wC = 0.0;
	double qA, qB;

	for (; i < i_last; i++) {
		qA = 1.0 - i->qBDecided;
		qB = i->qBDecided * (1.0 - gGiven) +
		     i->partner->qBDecided * gGiven;
		i->w = fmax(0.0, ces(qA, qB) - i->cost);
		wC += i->w;
		i->wCumulative = wC;

		i->age++;
		i->qBSeen = i->qBDecided;
		i->oldpartner = i->partner;
	}

	return wC;
}

double ces(double qA, double qB)
{
	double w;

	if (grho > -0.001 && grho < 0.001) {
		w = pow(qA, 1.0 - galpha) * pow(qB, galpha); // Cobb-Douglas
	} else {
		w = pow((1.0 - galpha) * pow(qA, grho) + galpha * pow(qB, grho),
			1.0 / grho);
	}

	return w;
}

void update_scores(struct itype *i, struct itype *i_last)
{
	for (; i < i_last; i++) {
		i->qBSeenSum += i->qBSeen;
		i->qBSeen_lt = i->qBSeenSum / i->age;
	}
}
