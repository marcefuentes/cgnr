#include <stdio.h>
#include <stdlib.h>
#include "sim.h"

int read_int(FILE *fp, const char *format, int *value, const char *error_message)
{
	if (fscanf(fp, format, value) != 1)
	{
		fprintf(stderr, "Error reading %s from file.\n", error_message);
		exit(EXIT_FAILURE);
	}
	return *value;
}

double read_double(FILE *fp, const char *format, double *value, const char *error_message)
{
	if (fscanf(fp, format, value) != 1)
	{
		fprintf(stderr, "Error reading %s from file.\n", error_message);
		exit(EXIT_FAILURE);
	}
	return *value;
}
