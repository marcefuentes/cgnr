#ifndef MATH_TOOLS_H
#define MATH_TOOLS_H

double ces(double qA, double qB, double alpha, double rho);
double pearson_r(double sum_x, double sum_y, double sum_xy, double sum_x2, double sum_y2, unsigned int n);
double quartile(double *frequencies, int num_bins, double quartile, int *bin, double *previous_freq);
int    select_bin(double bin_size, double value);
double stdev(double sum, double sum2, unsigned int num);

#endif  // MATH_TOOLS_H
