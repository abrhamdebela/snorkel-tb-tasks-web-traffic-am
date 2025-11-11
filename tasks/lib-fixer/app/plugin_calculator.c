/**
 * Calculator Plugin: Example plugin that depends on libmath_utils
 */

#include <stdio.h>

// Depends on libmath_utils
extern int add_numbers(int a, int b);
extern int multiply_numbers(int a, int b);

void plugin_init(void) {
    printf("[Calculator Plugin] Initializing...\n");
}

void plugin_run(void) {
    printf("[Calculator Plugin] Running calculations...\n");
    
    int result1 = add_numbers(100, 50);
    printf("  100 + 50 = %d\n", result1);
    
    int result2 = multiply_numbers(12, 8);
    printf("  12 * 8 = %d\n", result2);
    
    printf("[Calculator Plugin] Complete!\n");
}

