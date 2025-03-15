#include <stdio.h>

#include "io.h"

int write_time_elapsed(char *filename, float time_elapsed) {
    FILE *file = fopen(filename, "a+");
    if (file == NULL) {
        return file_write_error(filename);
    }

    fprintf(file, "TimeElapsed,");

    if (time_elapsed < 10.0) {
        fprintf(file, "%f", time_elapsed);
    } else {
        int minute = 60;
        int hour = minute * 60;
        int day = hour * 24;

        int seconds = (int)time_elapsed;
        int days = seconds / day;
        seconds -= days * day;
        int hours = seconds / hour;
        seconds -= hours * hour;
        int minutes = seconds / minute;
        seconds -= minutes * minute;

        if (days > 0) {
            fprintf(file, "%i-", days);

            if (hours < 10) {
                fprintf(file, "0");
            }
        }

        if (days > 0 || hours > 0) {
            fprintf(file, "%i:", hours);

            if (minutes < 10) {
                fprintf(file, "0");
            }
        }

        if (days > 0 || hours > 0 || minutes > 0) {
            fprintf(file, "%i:", minutes);

            if (seconds < 10) {
                fprintf(file, "0");
            }
        }

        fprintf(file, "%i", seconds);
    }

    fprintf(file, "\n");

    fclose(file);

    return 0;
}
