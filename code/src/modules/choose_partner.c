#include <gsl/gsl_rng.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "sim.h"

// Global variable
extern gsl_rng *rng;

struct List {
    unsigned int ind;
    struct List *next;
};

struct List *create_shuffled_list(unsigned int size);
void         free_list(struct List **head);
bool         willing(struct Individual *a, struct Individual *b);

int choose_partner(struct Individual *i_first, struct Individual *i_last, unsigned int groupsize) {
    for (struct Individual *i = i_first; i < i_last; i += groupsize) {
        struct List *head = create_shuffled_list(groupsize);
        if (head == NULL) {
            fprintf(stderr, "Failed create_shuffled_list (choose_partner).\n");
            free_list(&head);
            return -1;
        }

        while (head != NULL && head->next != NULL) {
            struct List       *previous = head;
            struct List       *temp = head->next;
            struct Individual *j = i + head->ind;
            struct Individual *k = i + temp->ind;

            while (temp != NULL && (willing(j, k) == false || willing(k, j) == false)) {
                previous = temp;
                temp = temp->next;
                if (temp != NULL) {
                    k = i + temp->ind;
                }
            }

            if (temp != NULL) {
                k->partner->partner = j->partner;
                j->partner->partner = k->partner;
                k->partner = j;
                j->partner = k;

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

    for (unsigned int c = 0; c < size; c++) {
        struct List *temp = malloc(sizeof(*temp));
        if (temp == NULL) {
            fprintf(stderr, "Failed malloc (create_shuffled_list).\n");
            return NULL;
        }

        temp->ind = (start + c) % size;
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

bool willing(struct Individual *a, struct Individual *b) {
    if (a == NULL || b == NULL || a->partner == NULL) {
        fprintf(stderr, "Null pointer encountered in willing.\n");
    }

    if ((b->qBSeen - a->partner->qBSeen > a->ChooseGrain) ||
        (b->qBSeen_lt - a->partner->qBSeen_lt > a->Choose_ltGrain)) {
        return true;
    }

    return false;
}
