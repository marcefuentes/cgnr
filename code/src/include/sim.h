#include <stdio.h>

#define BINS 64
#define CONTINUOUS_V 8
#define CORRELATIONS 15
#define MAX_FILENAME_LEN 20

// Structures

struct Aggregate {
    unsigned long time;
    double        alpha, logES, Given;
    double        mean[CONTINUOUS_V], mean2[CONTINUOUS_V];
    double        sd[CONTINUOUS_V], sd2[CONTINUOUS_V];
    double        frc[CONTINUOUS_V][BINS], frc2[CONTINUOUS_V][BINS];
    double        median[CONTINUOUS_V], median2[CONTINUOUS_V];
    double        iqr[CONTINUOUS_V], iqr2[CONTINUOUS_V];
    double        corr[CORRELATIONS], corr2[CORRELATIONS];
};

struct Individual {
    double             w;
    double             qBDefault;
    double             qBDecided;  // qB for next round
    double             qBSeen;     // qB in present round
    double             qBSeenSum;  // sum of qBSeen since birth
    double             qBSeen_lt;  // average qBSeen since birth
    double             wCumulative;
    double             ChooseGrain;
    double             Choose_ltGrain;
    double             MimicGrain;
    double             ImimicGrain;
    double             Imimic_ltGrain;
    double             cost;  // Information costs
    unsigned int       age;   // It can't be killed. It isn't known to, and doesn't know, group mates
    struct Individual *oldpartner;
    struct Individual *partner;
};

struct Recruit {
    double          randomwc;
    double          qBDefault;
    double          ChooseGrain;
    double          Choose_ltGrain;
    double          MimicGrain;
    double          ImimicGrain;
    double          Imimic_ltGrain;
    double          cost;
    struct Recruit *next;
};

// Functions

int             choose_partner(struct Individual *i, struct Individual *i_last, unsigned int groupsize);
struct Recruit *create_recruits(unsigned int deaths, double wc);
void            decide_qB(struct Individual *i, struct Individual *i_last, int imimic);
void            free_Recruit_list(struct Recruit **recruit);
void            kill(struct Recruit *recruit, struct Individual *i_first, unsigned int n);
int             read_key_value(FILE *fp, const char *expected_key, void *value, const char *type);
int             shuffle_partners(struct Individual *i, struct Individual *i_last, unsigned int groupsize);
void            stats_end(struct Aggregate *agg, struct Aggregate *agg_last, struct Aggregate *p);
void            stats_period(struct Individual *i, struct Individual *i_last, struct Aggregate *agg, unsigned int n);
void            stats_runs(struct Aggregate *p, struct Aggregate *aggall_last, unsigned int runs);
int             write_headers_csv(char *filename);
int             write_headers_frq(char *filename);
int             write_ics(char *filename, int sequence, float alpha, float logES, float Given, unsigned long t,
                          struct Individual *i, struct Individual *i_last);
int             write_stats_csv(char *filename, struct Aggregate *p, struct Aggregate *aggall_last);
int             write_stats_frq(char *filename, struct Aggregate *p, struct Aggregate *aggall_last);
int             write_time_elapsed(char *filename, float time_elapsed);
