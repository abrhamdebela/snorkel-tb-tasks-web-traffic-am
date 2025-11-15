#include <stdio.h>
#include <stdlib.h>
#include "utils.h"
#include "database.h"

#define VERSION "1.2.3"
#define PROGRAM_NAME "DataProcessor"

int main(int argc, char *argv[]) {
    printf("Starting %s v%s\n", PROGRAM_NAME, VERSION);

    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    printf("Initializing database connection...\n");
    if (initialize_database() != 0) {
        fprintf(stderr, "Failed to initialize database\n");
        return 1;
    }

    printf("Processing file: %s\n", argv[1]);
    int result = process_data_file(argv[1]);

    cleanup_database();

    if (result == 0) {
        printf("Processing completed successfully\n");
    } else {
        fprintf(stderr, "Processing failed with error code: %d\n", result);
    }

    return result;
}
