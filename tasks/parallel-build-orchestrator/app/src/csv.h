#ifndef CSV_H
#define CSV_H

#include <stdio.h>

typedef struct {
    int u, v;
    double w;
} edge_row_t;

// Returns 1 on success, 0 on EOF.
int csv_read_edge(FILE* f, edge_row_t* out);

#endif
