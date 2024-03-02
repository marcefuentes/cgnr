#include <stdio.h>
#include <stdlib.h>
#include <gsl/gsl_rng.h>
#include <math.h>
#include "sim.h"

// Global variable
extern gsl_rng *rng;

struct rtype *create_recruits(int deaths, double wc)
{
	struct rtype *temp, *head, *member;
	double random;

	head = NULL;

	for (int d = 0; d < deaths; d++)
	{
		temp = malloc(sizeof *temp);
		if (temp == NULL)
		{
			printf("\nFailed malloc (create_recruits)");
			exit(EXIT_FAILURE);
		}

		random = gsl_rng_uniform(rng);
		temp->randomwc = wc*random;
		temp->next = NULL;

		// Inserts into ascending randomwc

		if (head == NULL 
			|| head->randomwc >= temp->randomwc)
		{
			temp->next = head;
			head = temp;
		}
		else
		{
			member = head;

			while (member->next != NULL
				&& member->next->randomwc < temp->randomwc)
			{
				member = member->next;
			}

			temp->next = member->next;
			member->next = temp;
		}
	}

	return head;
}

void kill(struct rtype *recruit, struct itype *i_first, int n, double cost)
{
	struct itype *i;
	int pick;

	for (; recruit != NULL; recruit = recruit->next)
	{
		do
		{
			pick = gsl_rng_uniform_int(rng, n);	// Kills an individual...
		} while ((i_first + pick)->age == 0);	// ... that is not already dead

		i =			i_first + pick;
		i->qBDefault =		recruit->qBDefault;
		i->qBDecided =		i->qBDefault;
		i->qBSeenSum =		0.0;
		i->qBSeen_lt =		0.0;
		i->ChooseGrain =	recruit->ChooseGrain;
		i->Choose_ltGrain =	recruit->Choose_ltGrain;
		i->MimicGrain =		recruit->MimicGrain;
		i->ImimicGrain =	recruit->ImimicGrain;
		i->Imimic_ltGrain =	recruit->Imimic_ltGrain;
	        i->cost =		-cost*(log(i->ChooseGrain) +
					       log(i->Choose_ltGrain) +
					       log(i->MimicGrain) +
					       log(i->ImimicGrain) +
					       log(i->Imimic_ltGrain));
		i->age =		0;
	}
}

void free_recruits(struct rtype *head)
{
	struct rtype *member;

	while (head != NULL)
	{
		member = head;
		head = head->next;
		free(member);
	}
}

