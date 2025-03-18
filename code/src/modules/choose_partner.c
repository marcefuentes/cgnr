#include <gsl/gsl_rng.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "individual.h"

// Global variable
extern gsl_rng *rng;

typedef struct List {
    unsigned int ind;
    struct List *next;
} List;

List *create_shuffled_list(unsigned int size);
void  free_list(List **head);
bool  willing(Individual *ind_a, Individual *ind_b);

int choose_partner(Individual *ind_first, Individual *ind_last, unsigned int group_size) {
    for (Individual *ind = ind_first; ind < ind_last; ind += group_size) {
        List *head = create_shuffled_list(group_size);
        if (head == NULL) {
            fprintf(stderr, "Failed create_shuffled_list (choose_partner).\n");
            free_list(&head);
            return -1;
        }

        while (head != NULL && head->next != NULL) {
            List       *previous = head;
            List       *temp = head->next;
            Individual *ind_j = ind + head->ind;
            Individual *ind_k = ind + temp->ind;

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
            List *temp = head;
            head = NULL;
            free(temp);
        }
    }

    return 0;
}

List *create_shuffled_list(unsigned int size) {
    List        *head = NULL;
    unsigned int start = (unsigned int)gsl_rng_uniform_int(rng, size);

    for (unsigned int individual = 0; individual < size; individual++) {
        List *temp = malloc(sizeof(*temp));
        if (temp == NULL) {
            return NULL;
        }

        temp->ind = (start + individual) % size;
        temp->next = head;
        head = temp;
    }

    return head;
}

void free_list(List **head) {
    while (*head != NULL) {
        List *temp = *head;
        *head = (*head)->next;
        free(temp);
    }
}

bool willing(Individual *ind_a, Individual *ind_b) {
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
