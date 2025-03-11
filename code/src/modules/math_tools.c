#include <limits.h>
#include <math.h>
#include <stdio.h>

#define EPSILON 1e-6

double ces(double qA, double qB, double alpha, double rho) {
    double fitness;

    if (fabs(rho - 0.0) < EPSILON) {
        fitness = pow(qA, 1.0 - alpha) * pow(qB, alpha);  // Cobb-Douglas
    } else {
        fitness = pow(((1.0 - alpha) * pow(qA, rho)) + (alpha * pow(qB, rho)), 1.0 / rho);
    }

    return fitness;
}

double pearson_r(double sum_x, double sum_y, double sum_xy, double sum_x2, double sum_y2, unsigned int num) {
    double numerator = (num * sum_xy) - (sum_x * sum_y);
    double denominator = sqrt(((num * sum_x2) - (sum_x * sum_x)) * ((num * sum_y2) - (sum_y * sum_y)));
    double pearson_r = 0.0;

    if (denominator > 0.0) {
        pearson_r = numerator / denominator;
    }

    return pearson_r;
}

double quartile(double *frequencies, int num_bins, double percentile, int *bin, double *previous_freq) {
    double cumulative_freq = *previous_freq;
    double freq = 0.0;

    while (cumulative_freq < percentile) {
        if (*bin >= INT_MAX) {  // Prevent overflow
            fprintf(stderr, "Error: bin overflow in quartile.\n");
            return 0.0;  // Or other error handling
        }
        freq = frequencies[*bin];
        cumulative_freq += freq;
        (*bin)++;
    }

    if (cumulative_freq > percentile) {
        (*bin)--;
        cumulative_freq -= freq;  // Correct cumulativeFreq
    }

    *previous_freq = cumulative_freq;  // Update previousfreq
    double delta = frequencies[*bin];
    if (fabs(delta - 0.0) < EPSILON) {
        // Handle division by zero.
        fprintf(stderr, "Error: Division by zero in quartile.\n");
        return 0.0;
    }

    return ((double)*bin / num_bins) + ((percentile - cumulative_freq) / (delta * num_bins));
}

int select_bin(double bin_size, double value) {
    double ceiling = bin_size;
    int    bin = 0;

    while (value > ceiling) {
        ceiling += bin_size;
        bin++;
    }

    return bin;
}

double stdev(double sum, double sum2, unsigned int num) {
    if (num <= 1) {
        return 0.0;
    }

    double variance = (sum2 - (sum * sum / num)) / (num - 1);
    return (variance > 0.0) ? sqrt(variance) : 0.0;
}
