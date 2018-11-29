#include <stdio.h>
#include <time.h>
#include <omp.h>
#include <math.h>

// there will we max 2^k threads in the program
#define K 7
// how many time n_min will be multiplied by 2
#define N 4
#define NUM_OF_FUNCS 4

typedef double(*pointFunc)(double);

double f1(double x) {
    return 5;
}

double f2(double x) {
    return x;
}

double f3(double x) {
    return x*x*x - 3*x*x + 6*x - 3;
}

double f4(double x) {
    return cos(x) * exp(x) / (sqrt(x + 1) + 1);
}

double simpson_integral(pointFunc f, double a, double b, int n) {
    const double h = (b - a) / n;
    double k1 = 0, k2 = 0;
    #pragma omp parallel for reduction(+:k1, k2)
    for (int i = 1; i < n; i += 2) {
        k1 += f(a + i * h);
        k2 += f(a + (i + 1) * h);
    }
    return h / 3 * (f(a) + 4 * k1 + 2 * k2 + f(b));
}

double evaluate(pointFunc f, double a, double b, int n, int threads_num) {

    omp_set_num_threads(threads_num);

    double timer = omp_get_wtime();
    double result = simpson_integral(f, a, b, n);
    double time = omp_get_wtime() - timer;

    printf("Test with %d thread%c\n", threads_num, threads_num == 1 ? ' ' : 's');
    printf("Result: %f\n", result);
    printf("Time: %fs\n\n", time);
    return time;
}

int main() {

    // define segment of integration [a, b]
    int a = 0, b = 1;

    // number of blocks we divide our interval into
    int n_min = 100000000;

    int max_threads = 1 << K;

    double result = 0;

    int iterations = 3;

    double results[NUM_OF_FUNCS][N][K+1] = {0};

    pointFunc funcs[NUM_OF_FUNCS] = {f1, f2, f3, f4};

    for (int func_i = 0; func_i < NUM_OF_FUNCS; func_i++) {
        printf("Testing %d function\n", func_i+1);
        printf("-------------------\n\n");
        for (int n = n_min, n_i = 0; n_i < N; n *= 2, n_i++) {
            printf("Testing with segment divided in %d pieces\n", n);
            printf("-------------------\n\n");
            for (int iter = 0; iter < iterations; iter++) {
                printf("%d iteration\n", iter+1);
                printf("*******************\n\n");
                for (int threads = 1, k = 0; threads <= max_threads; threads *= 2, k++) {
                    results[func_i][n_i][k] += evaluate(funcs[func_i], a, b, n, threads);
                }
            }
        }
    }

    printf("Printing final mean time results\n");
    printf("*******************\n\n");
    for (int func_i = 0; func_i < NUM_OF_FUNCS; func_i++) {
        printf("Function %d\n", func_i+1);
        for (int n_i = 0; n_i < N; n_i++) {
            for (int k = 0; k < K+1;  k++) {
                printf("%f, ", results[func_i][n_i][k] / iterations);
            }
        }
        printf("\n");
    }
    return 0;
}
