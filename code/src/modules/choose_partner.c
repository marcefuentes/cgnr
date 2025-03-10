#include <gsl/gsl_rng.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "individual.h"

// Global variable
extern gsl_rng *rng;

struct List {
    unsigned int ind;
    struct List *next;
};

struct List *create_shuffled_list(unsigned int size);
void         free_list(struct List **head);
bool         willing(struct Individual *ind_a, struct Individual *ind_b);

int choose_partner(struct Individual *ind_first, struct Individual *ind_last, unsigned int groupsize) {
    for (struct Individual *ind = ind_first; ind < ind_last; ind += groupsize) {
        struct List *head = create_shuffled_list(groupsize);
        if (head == NULL) {
            fprintf(stderr, "Failed create_shuffled_list (choose_partner).\n");
            free_list(&head);
            return -1;
        }

        while (head != NULL && head->next != NULL) {
            struct List       *previous = head;
            struct List       *temp = head->next;
            struct Individual *ind_j = ind + head->ind;
            struct Individual *ind_k = ind + temp->ind;

            while (temp != NULL && (willing(ind_j, ind_k) == false || willing(ind_k, ind_j) == false)) {
                previous = temp;
                temp = temp->next;
                if (temp != NULL) {
                    ind_k = ind + temp->ind;
                }
            }

            if (temp != NULL) {
                ind_k->partner->partner = ind_j->partner;
                ind_j->partner->partner = ind_k->partner;
                ind_k->partner = ind_j;
                ind_j->partner = ind_k;

                previous->next = temp->next;

                free(temp);
            }

            temp = head;
            head = head->next;
            free(temp);
        }

        if (head != NULL) {
            struct List *temp = head;
            head = NULL;
            free(temp);
        }
    }

    return 0;
}

struct List *create_shuffled_list(unsigned int size) {
    struct List *head = NULL;
    unsigned int start = (unsigned int)gsl_rng_uniform_int(rng, size);

    for (unsigned int individual = 0; individual < size; individual++) {
        struct List *temp = malloc(sizeof(*temp));
        if (temp == NULL) {
            fprintf(stderr, "Failed malloc (create_shuffled_list).\n");
            return NULL;
        }

        temp->ind = (start + individual) % size;
        temp->next = head;
        head = temp;
    }

    return head;
}

void free_list(struct List **head) {
    while (*head != NULL) {
        struct List *temp = *head;
        *head = (*head)->next;
        free(temp);
    }
}

bool willing(struct Individual *ind_a, struct Individual *ind_b) {
    if (ind_a == NULL || ind_b == NULL || ind_a->partner == NULL) {
        fprintf(stderr, "Null pointer encountered in willing.\n");
        return false;
    }

    if ((ind_b->qBSeen - ind_a->partner->qBSeen > ind_a->ChooseGrain) ||
        (ind_b->qBSeen_lt - ind_a->partner->qBSeen_lt > ind_a->Choose_ltGrain)) {
        return true;
    }

    return false;
}
