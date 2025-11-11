/**
 * Logger Plugin: Example plugin that depends on libstring_utils
 */

#include <stdio.h>

// Depends on libstring_utils
extern void to_uppercase(char* str);

void plugin_init(void) {
    printf("[Logger Plugin] Initializing...\n");
}

void plugin_run(void) {
    printf("[Logger Plugin] Running...\n");
    
    char message[] = "plugin logging system active";
    printf("  Original message: %s\n", message);
    
    to_uppercase(message);
    printf("  Uppercased message: %s\n", message);
    
    printf("[Logger Plugin] Complete!\n");
}

