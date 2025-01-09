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

int read_globals(char *filename);
int caso(struct ptype *p_first, char *filename);
void start_population(struct itype *i, struct itype *i_last);
double fitness(struct itype *i, struct itype *i_last);
double ces(double qA, double qB); // glogES, galpha
void update_scores(struct itype *i, struct itype *i_last);
void free_memory(struct itype *i_first, struct pruntype *prun_first);

int main(int argc, char *argv[])
{
	clock_t start = clock();

	if (argc != 2) {
		fprintf(stderr, "You must run the program with an argument.\n");
		exit(EXIT_FAILURE);
	}

	if (strlen(argv[1]) > 8) {
		fprintf(stderr,
			"The argument must have fewer than 8 characters.\n");
		exit(EXIT_FAILURE);
	}

	char csv[MAX_FILENAME_LEN];
	char frq[MAX_FILENAME_LEN];
	char glo[MAX_FILENAME_LEN];
	char ics[MAX_FILENAME_LEN];
	const char *filename = argv[1];
	snprintf(csv, sizeof(csv), "%s.csv", filename);
	snprintf(frq, sizeof(frq), "%s.frq", filename);
	snprintf(glo, sizeof(glo), "%s.glo", filename);
	snprintf(ics, sizeof(ics), "%s.ics", filename);

	if (write_headers_csv(csv) < 0) {
		fprintf(stderr, "Failed write_headers_csv.\n");
		exit(EXIT_FAILURE);
	}
	if (write_headers_frq(frq) < 0) {
		fprintf(stderr, "Failed write_headers_frq.\n");
		exit(EXIT_FAILURE);
	}
	if (read_globals(glo) < 0) {
		fprintf(stderr, "Failed read_globals.\n");
		exit(EXIT_FAILURE);
	}

	rng = gsl_rng_alloc(gsl_rng_taus);
	if (rng == NULL) {
		fprintf(stderr, "Failed gsl_rng_alloc.\n");
		exit(EXIT_FAILURE);
	}

	if (gSeed == 1) {
		struct timeval tv;
		gettimeofday(&tv, 0);
		gsl_rng_set(rng, tv.tv_sec + tv.tv_usec);
	}

	struct ptype *p_first = calloc(gPeriods + 1, sizeof(*p_first));
	if (p_first == NULL) {
		fprintf(stderr, "Failed calloc (periods).\n");
		gsl_rng_free(rng);
		exit(EXIT_FAILURE);
	}

	struct ptype *p_last = p_first + gPeriods + 1;

	if (caso(p_first, ics) < 0) {
		fprintf(stderr, "Failed caso.\n");
		gsl_rng_free(rng);
		free(p_first);
		exit(EXIT_FAILURE);
	}

	stats_runs(p_first, p_last, gRuns);
	if (write_stats_csv(csv, p_first, p_last) < 0) {
		fprintf(stderr, "Failed write_stats_csv.\n");
		gsl_rng_free(rng);
		free(p_first);
		exit(EXIT_FAILURE);
	}
	if (write_stats_frq(frq, p_first, p_last) < 0) {;
		fprintf(stderr, "Failed write_stats_frq.\n");
		gsl_rng_free(rng);
		free(p_first);
		exit(EXIT_FAILURE);
	}

	free(p_first);

	gsl_rng_free(rng);

	if (write_time_elapsed(glo, (float)(clock() - start) / CLOCKS_PER_SEC) < 0) {
		fprintf(stderr, "Failed write_time_elapsed.\n");
		exit(EXIT_FAILURE);
	}

	return 0;
}

int read_globals(char *filename)
{
	FILE *fp;

	if ((fp = fopen(filename, "r")) == NULL) {
		fprintf(stderr, "Failed to open file %s for reading.\n", filename);
		return -1;
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

	return 0;
}

int caso(struct ptype *p_first, char *filename)
{
	int sequence = 0;

	for (int r = 0; r < gRuns; r++) {
		struct itype *i_first = calloc(gN, sizeof(*i_first));
		if (i_first == NULL) {
			fprintf(stderr, "Failed calloc (individuals).\n");
			return -1;
		}

		struct itype *i_last = i_first + gN;

		struct pruntype *prun_first = calloc(gPeriods + 1, sizeof(*prun_first));
		if (prun_first == NULL) {
			fprintf(stderr, "Failed calloc (periods of each run).\n");
			free_memory(i_first, prun_first);
			return -1;
		}

		struct pruntype *prun_last = prun_first + gPeriods + 1;
		struct pruntype *prun = prun_first;

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
				if (gRuns == 1) {
					write_ics(filename, sequence, (float)galpha,
						(float)glogES, (float)gGiven,
						t + 1, i_first, i_last);
					sequence++;
				}
			}

			if (gLanguage == 1) {
				update_scores(i_first, i_last);
			}

			if (gShuffle == 1) {
				if (shuffle_partners(i_first, i_last, gGroupSize) < 0) {
					fprintf(stderr, "Failed shuffle_partners.\n");
					free_memory(i_first, prun_first);
					return -1;
				}
			}

			if (gPartnerChoice == 1) {
				if (choose_partner(i_first, i_last, gGroupSize) < 0) {
					fprintf(stderr, "Failed choose_partner.\n");
					free_memory(i_first, prun_first);
					return -1;
				}
			}

			int deaths = gsl_ran_binomial(rng, gDeathRate, gN);

			if (deaths > 0) {
				struct rtype *recruit_first =
					create_recruits(deaths, wC);
				if (recruit_first == NULL) {
					fprintf(stderr, "Failed create_recruits.\n");
					free_memory(i_first, prun_first);
					return -1;
				}
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
				free_rtype_list(&recruit_first);
			}

			if (gReciprocity == 1) {
				decide_qB(i_first, i_last, gIndirectR);
			}
		}

		stats_end(prun_first, prun_last, p_first);
		free_memory(i_first, prun_first);
	}

	return 0;
}

void start_population(struct itype *i, struct itype *i_last)
{
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

	for (struct itype *j = i + 1; j < i_last; j++) {
		*j = *i;
	}

	for (struct itype *j = i + 1; i < i_last; i += 2, j += 2) {
		i->partner = j;
		j->partner = i;
	}
}

double fitness(struct itype *i, struct itype *i_last)
{
	double wC = 0.0;

	for (; i < i_last; i++) {
		double qA = 1.0 - i->qBDecided;
		double qB = i->qBDecided * (1.0 - gGiven) +
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

void free_memory(struct itype *i_first, struct pruntype *prun_first)
{
	free(i_first);
	i_first = NULL;
	free(prun_first);
	prun_first = NULL;
}
