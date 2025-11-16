#include <stdio.h>
#include <string.h>

// This file is a decoy - it won't be linked into the binary
// Used to test the matching algorithm

void unused_function(void) {
    printf("This function is never called\n");
}

int compute_checksum(const char *data) {
    int checksum = 0;
    for (int i = 0; data[i] != '\0'; i++) {
        checksum += data[i];
    }
    return checksum;
}
