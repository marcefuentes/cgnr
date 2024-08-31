#include <stdio.h>

#define CONTINUOUS_V 8
#define CORRELATIONS 15
#define BINS 64

// Structures

struct ptype {
	int time;
	double alpha, logES, Given;
	double mean[CONTINUOUS_V], mean2[CONTINUOUS_V];
	double sd[CONTINUOUS_V], sd2[CONTINUOUS_V];
	double c[CONTINUOUS_V][BINS], c2[CONTINUOUS_V][BINS];
	double median[CONTINUOUS_V], median2[CONTINUOUS_V];
	double iqr[CONTINUOUS_V], iqr2[CONTINUOUS_V];
	double corr[CORRELATIONS], corr2[CORRELATIONS];
};

struct pruntype {
	int time;
	double alpha, logES, Given;
	double mean[CONTINUOUS_V];
	double sd[CONTINUOUS_V];
	double frc[CONTINUOUS_V][BINS];
	double median[CONTINUOUS_V];
	double iqr[CONTINUOUS_V];
	double corr[CORRELATIONS];
};

struct itype {
	double w;
	double qBDefault;
	double qBDecided; // qB for next round
	double qBSeen; // qB in present round
	double qBSeenSum; // sum of qBSeen since birth
	double qBSeen_lt; // average qBSeen since birth
	double wCumulative;
	double ChooseGrain;
	double Choose_ltGrain;
	double MimicGrain;
	double ImimicGrain;
	double Imimic_ltGrain;
	double cost; // Information costs
	int age; // It can't be killed. It isn't known to, and doesn't know, group mates
	struct itype *oldpartner;
	struct itype *partner;
};

struct rtype {
	double randomwc;
	double qBDefault;
	double ChooseGrain;
	double Choose_ltGrain;
	double MimicGrain;
	double ImimicGrain;
	double Imimic_ltGrain;
	struct rtype *next;
};

// Functions

void decide_qB(struct itype *i, struct itype *i_last, int imimic);
void shuffle_partners(struct itype *i, struct itype *i_last, int groupsize);
void choose_partner(struct itype *i, struct itype *i_last, int groupsize);
struct rtype *create_recruits(int deaths, double wc);
void free_recruits(struct rtype *recruit);
void kill(struct rtype *recruit, struct itype *i_first, int n, double cost);
void stats_period(struct itype *i, struct itype *i_last, struct pruntype *prun,
		  int n);
void stats_end(struct pruntype *prun, struct pruntype *prun_last,
	       struct ptype *p);
void stats_runs(struct ptype *p, struct ptype *p_last, int runs);
int read_int(FILE *fp, const char *format, int *value,
	     const char *error_message);
double read_double(FILE *fp, const char *format, double *value,
		   const char *error_message);
void write_headers_csv(char *filename);
void write_headers_i(char *filename);
void write_headers_frq(char *filename);
void write_stats_csv(char *filename, struct ptype *p, struct ptype *p_last);
void write_stats_frq(char *filename, struct ptype *p, struct ptype *p_last);
void write_i(char *filename, float alpha, float logES, float Given, int t,
	     struct itype *i, struct itype *i_last);
void write_time_elapsed(char *filename, float time_elapsed);
void file_write_error(char *filename);
