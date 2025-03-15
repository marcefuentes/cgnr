#include <stdio.h>

#include "io.h"

const char *headers =
    "alpha,logES,Given,Time,qBDefault,qBDecided,qBSeen,qBSeen_j,w,ChooseGrain,Choose_ltGrain,MimicGrain,ImimicGrain,"
    "Imimic_ltGrain,cost,age";

int write_ics(char *filename, int sequence, float alpha, float logES, float Given, unsigned long time,
              struct Individual *ind, struct Individual *ind_last) {
    char new_filename[18];

    snprintf(new_filename, sizeof(new_filename), "%s_%04d.ics", filename, sequence);

    FILE *file = fopen(new_filename, "a+");
    if (file == NULL) {
        return file_write_error(new_filename);
    }

    fprintf(file, "%s", headers);

    for (; ind < ind_last; ind++) {
        fprintf(file, "\n%f,%f,%f,%lu,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%i", alpha, logES, Given, time, ind->qBDefault,
                ind->qBDecided, ind->qBSeen, ind->partner->qBSeen, ind->w, ind->ChooseGrain, ind->Choose_ltGrain,
                ind->MimicGrain, ind->ImimicGrain, ind->Imimic_ltGrain, ind->cost, ind->age);
    }

    fprintf(file, "\n");
    fclose(file);

    return 0;
}
