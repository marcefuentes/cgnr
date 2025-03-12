#include <gsl/gsl_rng.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "dtnorm.h"  // From https://github.com/alanrogers/dtnorm
#include "individual.h"
#include "recruit.h"

// Global variable
extern gsl_rng *rng;

struct Recruit *create_recruits(unsigned int deaths, double w_cumulative) {
    struct Recruit *head = NULL;

    for (unsigned int death = 0; death < deaths; death++) {
        struct Recruit *temp = malloc(sizeof(*temp));
        if (temp == NULL) {
            fprintf(stderr, "Failed malloc (create_recruits).\n");
            free_recruit_list(&head);
            return NULL;
        }

        double random = gsl_rng_uniform(rng);
        temp->randomwc = w_cumulative * random;
        temp->next = NULL;

        // Inserts into ascending randomwc

        if (head == NULL || head->randomwc >= temp->randomwc) {
            temp->next = head;
            head = temp;
        } else {
            struct Recruit *member = head;

            while (member->next != NULL && member->next->randomwc < temp->randomwc) {
                member = member->next;
            }

            temp->next = member->next;
            member->next = temp;
        }
    }

    return head;
}

void kill(struct Recruit *recruit, struct Individual *ind_first, unsigned int population_size) {
    unsigned int pick;

    for (; recruit != NULL; recruit = recruit->next) {
        do {
            pick = (unsigned int)gsl_rng_uniform_int(rng,
                                                     population_size);  // Kills an individual...
        } while ((ind_first + pick)->age == 0);  // ... that is not already dead

        struct Individual *ind = ind_first + pick;
        ind->qBDefault = recruit->qBDefault;
        ind->qBDecided = ind->qBDefault;
        ind->qBSeenSum = 0.0;
        ind->qBSeen_lt = 0.0;
        ind->ChooseGrain = recruit->ChooseGrain;
        ind->Choose_ltGrain = recruit->Choose_ltGrain;
        ind->MimicGrain = recruit->MimicGrain;
        ind->ImimicGrain = recruit->ImimicGrain;
        ind->Imimic_ltGrain = recruit->Imimic_ltGrain;
        ind->cost = recruit->cost;
        ind->age = 0;
    }
}

void mutate(struct Individual *ind, struct Recruit *recruit, double qb_mutation_size, double grain_mutation_size,
            double cost, int language) {
    for (; recruit != NULL; recruit = recruit->next) {
        while (recruit->randomwc > ind->wCumulative) {
            ind++;
        }

        recruit->qBDefault = dtnorm(ind->qBDefault, qb_mutation_size, 0.0, 1.0, rng);
        recruit->ChooseGrain = dtnorm(ind->ChooseGrain, grain_mutation_size, 0.0, 1.0, rng);
        recruit->MimicGrain = dtnorm(ind->MimicGrain, grain_mutation_size, 0.0, 1.0, rng);
        recruit->ImimicGrain = dtnorm(ind->ImimicGrain, grain_mutation_size, 0.0, 1.0, rng);
        if (language == 1) {
            recruit->Choose_ltGrain = dtnorm(ind->Choose_ltGrain, grain_mutation_size, 0.0, 1.0, rng);
            recruit->Imimic_ltGrain = dtnorm(ind->Imimic_ltGrain, grain_mutation_size, 0.0, 1.0, rng);
        } else {
            recruit->Choose_ltGrain = ind->Choose_ltGrain;
            recruit->Imimic_ltGrain = ind->Imimic_ltGrain;
        }

        recruit->cost = -cost * (log(recruit->ChooseGrain) + log(recruit->Choose_ltGrain) + log(recruit->MimicGrain) +
                                 log(recruit->ImimicGrain) + log(recruit->Imimic_ltGrain));
    }
}

void free_recruit_list(struct Recruit **head) {
    while (*head != NULL) {
        struct Recruit *temp = *head;
        *head = (*head)->next;
        free(temp);
    }
}
