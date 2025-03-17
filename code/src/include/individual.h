#ifndef INDIVIDUAL_H
#define INDIVIDUAL_H

struct Individual {
    unsigned int       age;
    double             qBDefault;
    double             qBDecided;
    double             qBSeen;
    double             qBSeenSum;
    double             qBSeen_lt;
    double             ChooseGrain;
    double             Choose_ltGrain;
    double             MimicGrain;
    double             ImimicGrain;
    double             Imimic_ltGrain;
    double             cost;
    double             w;
    double             wCumulative;
    struct Individual *oldpartner;
    struct Individual *partner;
};

#define INITIAL_INDIVIDUAL                      \
    ((struct Individual){.age = 0,              \
                         .qBDefault = 0.1,      \
                         .qBDecided = 0.1,      \
                         .qBSeen = 0.1,         \
                         .qBSeenSum = 0.0,      \
                         .qBSeen_lt = 0.0,      \
                         .ChooseGrain = 1.0,    \
                         .Choose_ltGrain = 1.0, \
                         .MimicGrain = 1.0,     \
                         .ImimicGrain = 1.0,    \
                         .Imimic_ltGrain = 1.0, \
                         .cost = 0.0,           \
                         .w = 0.0,              \
                         .wCumulative = 0.0,    \
                         .oldpartner = NULL,    \
                         .partner = NULL})

// Functions for handling individuals
int  choose_partner(struct Individual *ind, struct Individual *ind_last, unsigned int group_size);
int  choose_partner2(struct Individual *ind[], struct Individual *ind_last[], unsigned int group_size);
void decide_qB(struct Individual *ind, struct Individual *ind_last, int indirect_r);
int  shuffle_partners(struct Individual *ind, struct Individual *ind_last, unsigned int group_size);
int  shuffle_partners2(struct Individual *ind[], struct Individual *ind_last[], unsigned int group_size);
void update_scores(struct Individual *ind, struct Individual *ind_last);

#endif  // INDIVIDUAL_H
