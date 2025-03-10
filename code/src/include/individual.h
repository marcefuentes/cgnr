#ifndef INDIVIDUAL_H
#define INDIVIDUAL_H

struct Individual {
    double             w;
    double             qBDefault;
    double             qBDecided;
    double             qBSeen;
    double             qBSeenSum;
    double             qBSeen_lt;
    double             wCumulative;
    double             ChooseGrain;
    double             Choose_ltGrain;
    double             MimicGrain;
    double             ImimicGrain;
    double             Imimic_ltGrain;
    double             cost;
    unsigned int       age;
    struct Individual *oldpartner;
    struct Individual *partner;
};

// Functions for handling individuals
int  choose_partner(struct Individual *ind, struct Individual *ind_last, unsigned int groupsize);
void decide_qB(struct Individual *ind, struct Individual *ind_last, int imimic);
int  shuffle_partners(struct Individual *ind, struct Individual *ind_last, unsigned int groupsize);

#endif
