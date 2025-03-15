#ifndef GLOBALS_H
#define GLOBALS_H

struct GlobalVariables {
    int           seed;
    unsigned int  population_size;
    unsigned int  runs;
    unsigned long time;
    unsigned int  periods;
    double        qb_mutation_size;
    double        grain_mutation_size;
    double        death_rate;
    unsigned int  group_size;
    double        cost;
    int           partner_choice;
    int           reciprocity;
    int           indirect_r;
    int           language;
    int           shuffle;
    double        alpha;
    double        loges;
    double        given;
    double        rho;
    unsigned long time_per_period;
};

extern struct GlobalVariables globals;

int read_globals(const char *filename);

#endif  // GLOBALS_H
