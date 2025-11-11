/**
 * Test Application: test_app
 * Application that depends on custom libraries
 */

#include <stdio.h>
#include <string.h>

extern int add_numbers(int a, int b);
extern int multiply_numbers(int a, int b);
extern void reverse_string(char* str);
extern int count_vowels(const char* str);

int main(int argc, char* argv[]) {
    printf("=== Test Application ===\n\n");
    
    printf("Math Operations:\n");
    int sum = add_numbers(10, 20);
    printf("  10 + 20 = %d\n", sum);
    
    int product = multiply_numbers(5, 7);
    printf("  5 * 7 = %d\n", product);
    
    printf("\nString Operations:\n");
    char test_str[] = "Hello World";
    printf("  Original: %s\n", test_str);
    
    int vowel_count = count_vowels(test_str);
    printf("  Vowel count: %d\n", vowel_count);
    
    reverse_string(test_str);
    printf("  Reversed: %s\n", test_str);
    
    printf("\n=== All tests passed! ===\n");
    
    return 0;
}

