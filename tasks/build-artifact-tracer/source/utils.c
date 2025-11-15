#include "utils.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int process_data_file(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Error: Could not open file %s\n", filename);
        return -1;
    }

    char buffer[1024];
    int line_count = 0;

    while (fgets(buffer, sizeof(buffer), fp)) {
        line_count++;
        if (strlen(buffer) > 0) {
            process_line(buffer);
        }
    }

    fclose(fp);
    printf("Processed %d lines from file\n", line_count);

    return 0;
}

void process_line(const char *line) {
    // Simple processing logic
    if (strstr(line, "ERROR") != NULL) {
        fprintf(stderr, "Found error in line: %s", line);
    }
}

char* get_config_value(const char *key) {
    static char value[256];
    snprintf(value, sizeof(value), "config_value_for_%s", key);
    return value;
}
