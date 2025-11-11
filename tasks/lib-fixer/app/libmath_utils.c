/**
 * Test Library: libmath_utils.so
 * Simple math utilities library for testing dynamic linking
 */

#include <stdio.h>

int add_numbers(int a, int b) {
    return a + b;
}

int multiply_numbers(int a, int b) {
    return a * b;
}

double divide_numbers(double a, double b) {
    if (b == 0.0) {
        fprintf(stderr, "Error: Division by zero\n");
        return 0.0;
    }
    return a / b;
}

void print_version(void) {
    printf("libmath_utils version 1.2.3\n");
}

