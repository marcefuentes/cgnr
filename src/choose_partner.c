#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <gsl/gsl_rng.h>
#include "sim.h"

// Global variable
extern gsl_rng *rng;

struct gtype {
	int ind;
	struct gtype *next;
} ;

struct gtype *create_shuffled_list(int groupsize);
void free_gtype_list(struct gtype **head);
bool willing(struct itype *a, struct itype *b);

int choose_partner(struct itype *i_first, struct itype *i_last, int groupsize)
{
	for (struct itype *i = i_first; i < i_last; i += groupsize) {
		struct gtype *head = NULL;

		head = create_shuffled_list(groupsize);
		if (head == NULL) {
			fprintf(stderr, "\nFailed create_shuffled_list (choose_partner).");
			free_gtype_list(&head);
			return -1;
		}

		while (head != NULL && head->next != NULL) {
			struct gtype *previous = head;
			struct gtype *temp = head->next;
			struct itype *j = i +
			    head->ind; // j is a nickname of i + head->ind to make the lines below more readable
			struct itype *k = i +
			    temp->ind; // k is a nickname of i + temp->ind to make the lines below more readable

			while (temp != NULL &&
			    (willing(j, k) == false || willing(k, j) == false)) {
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
			struct gtype *temp = head;
			head = NULL;
			free(temp);
		}

	}

	return 0;
}

struct gtype *create_shuffled_list(int groupsize)
{
	struct gtype *head = NULL;
	int start = gsl_rng_uniform_int(rng, groupsize);

	for (int c = 0; c < groupsize; c++) {
		struct gtype *temp = malloc(sizeof(*temp));
		if (temp == NULL) {
			fprintf(stderr, "\nFailed malloc (create_shuffled_list).");
			free_gtype_list(&head);
			return NULL;
		}

		temp->ind = (start + c) % groupsize;
		temp->next = head;
		head = temp;
	}

	return head;
}

void free_gtype_list(struct gtype **head)
{
	while (*head != NULL) {
		struct gtype *temp = *head;
		*head = (*head)->next;
		free(temp);
	}
}

bool willing(struct itype *a, struct itype *b)
{
	if (a == NULL || b == NULL || a->partner == NULL) {
		fprintf(stderr, "\nNull pointer encountered in willing().");
	}

	if ((b->qBSeen - a->partner->qBSeen > a->ChooseGrain) ||
	    (b->qBSeen_lt - a->partner->qBSeen_lt > a->Choose_ltGrain)) {
		return true;
	}

	return false;
}
