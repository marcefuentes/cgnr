#include <stdio.h>

enum { BINS = 64, CONTINUOUS_V = 8, PAIRS = 15, MAX_FILENAME_LEN = 22 };

// Structures

struct Aggregate {
    unsigned long time;
    double        alpha, logES, Given;
    double        mean[CONTINUOUS_V], mean2[CONTINUOUS_V];
    double        sd[CONTINUOUS_V], sd2[CONTINUOUS_V];
    double        frc[CONTINUOUS_V][BINS], frc2[CONTINUOUS_V][BINS];
    double        median[CONTINUOUS_V], median2[CONTINUOUS_V];
    double        iqr[CONTINUOUS_V], iqr2[CONTINUOUS_V];
    double        corr[PAIRS], corr2[PAIRS];
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

int             choose_partner(struct Individual *ind, struct Individual *ind_last, unsigned int groupsize);
struct Recruit *create_recruits(unsigned int deaths, double wcumulative);
void            decide_qB(struct Individual *ind, struct Individual *ind_last, int imimic);
void            free_recruit_list(struct Recruit **head);
void            kill(struct Recruit *recruit, struct Individual *ind_first, unsigned int n);
int             read_key_value(FILE *file_pointer, const char *expected_key, void *value, const char *type);
int             shuffle_partners(struct Individual *ind, struct Individual *ind_last, unsigned int groupsize);
void            stats_end(struct Aggregate *agg, struct Aggregate *agg_last, struct Aggregate *aggall);
void stats_period(struct Individual *ind, struct Individual *ind_last, struct Aggregate *agg, unsigned int n);
void stats_runs(struct Aggregate *aggall, struct Aggregate *aggall_last, unsigned int runs);
int  write_headers_csv(char *filename);
int  write_headers_frq(char *filename);
int  write_stats_csv(char *filename, struct Aggregate *aggall, struct Aggregate *aggall_last);
int  write_stats_frq(char *filename, struct Aggregate *aggall, struct Aggregate *aggall_last);
int  write_time_elapsed(char *filename, float time_elapsed);
int  write_ics(char *filename, int sequence, float alpha, float logES, float Given, unsigned long time,
               struct Individual *ind, struct Individual *ind_last);
