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
int  choose_partner(struct Individual *ind, struct Individual *ind_last, unsigned int group_size);
int  choose_partner2(struct Individual *ind[], struct Individual *ind_last[], unsigned int group_size);
void decide_qB(struct Individual *ind, struct Individual *ind_last, int indirect_r);
int  shuffle_partners(struct Individual *ind, struct Individual *ind_last, unsigned int group_size);
int  shuffle_partners2(struct Individual *ind[], struct Individual *ind_last[], unsigned int group_size);
void update_scores(struct Individual *ind, struct Individual *ind_last);

#endif  // INDIVIDUAL_H
