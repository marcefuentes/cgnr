#include <gsl/gsl_rng.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "sim.h"

// Global variable
extern gsl_rng *rng;

struct Recruit *create_recruits(unsigned int deaths, double wc) {
    struct Recruit *head = NULL;

    for (unsigned int d = 0; d < deaths; d++) {
        struct Recruit *temp = malloc(sizeof(*temp));
        if (temp == NULL) {
            fprintf(stderr, "Failed malloc (create_recruits).\n");
            return NULL;
        }

        double random = gsl_rng_uniform(rng);
        temp->randomwc = wc * random;
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

void kill(struct Recruit *recruit, struct Individual *i_first, unsigned int n) {
    unsigned int pick;

    for (; recruit != NULL; recruit = recruit->next) {
        do {
            pick = (unsigned int)gsl_rng_uniform_int(rng,
                                                     n);  // Kills an individual...
        } while ((i_first + pick)->age == 0);  // ... that is not already dead

        struct Individual *i = i_first + pick;
        i->qBDefault = recruit->qBDefault;
        i->qBDecided = i->qBDefault;
        i->qBSeenSum = 0.0;
        i->qBSeen_lt = 0.0;
        i->ChooseGrain = recruit->ChooseGrain;
        i->Choose_ltGrain = recruit->Choose_ltGrain;
        i->MimicGrain = recruit->MimicGrain;
        i->ImimicGrain = recruit->ImimicGrain;
        i->Imimic_ltGrain = recruit->Imimic_ltGrain;
        i->cost = recruit->cost;
        i->age = 0;
    }
}

void free_Recruit_list(struct Recruit **head) {
    while (*head != NULL) {
        struct Recruit *temp = *head;
        *head = (*head)->next;
        free(temp);
    }
}
