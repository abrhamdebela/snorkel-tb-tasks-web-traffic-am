#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "graph.h"
#include "csv.h"
#include "dijkstra.h"
#include "../cpp/hash_c_api.h"

static void usage(const char* argv0) {
    fprintf(stderr, "usage: %s <n_vertices> <edges.csv> <src> <dst>\n", argv0);
    exit(2);
}

static void print_path(int* parent, int v) {
    if (v < 0) return;
    if (parent[v] != -1) print_path(parent, parent[v]);
    printf("%d ", v);
}

int main(int argc, char** argv) {
    if (argc < 5) usage(argv[0]);
    int n = atoi(argv[1]);
    const char* csv = argv[2];
    int src = atoi(argv[3]);
    int dst = atoi(argv[4]);

    FILE* f = fopen(csv, "r");
    if (!f) { perror("fopen"); return 1; }

    graph_t* g = graph_new((size_t)n);
    edge_row_t row;
    size_t m = 0;
    while (csv_read_edge(f, &row)) {
        if (row.u >= 0 && row.u < n && row.v >= 0 && row.v < n) {
            graph_add_edge(g, row.u, row.v, row.w);
            ++m;
        }
    }
    fclose(f);

    // Use C++ hash via C API for a simple sanity report
    char meta[128];
    snprintf(meta, sizeof meta, "graph:%d:%zu", n, m);
    unsigned long long h = (unsigned long long)hash_str(meta);

    printf("Loaded graph with %d vertices, %zu edges. meta-hash=%llu\n", n, m, h);

    int* parent = (int*)malloc((size_t)n * sizeof(int));
    double dist = 0.0;
    int rc = dijkstra(g, src, dst, &dist, parent);
    if (rc != 0) {
        printf("No path from %d to %d\n", src, dst);
        graph_free(g);
        free(parent);
        return 0;
    }
    printf("Shortest distance %d -> %d = %.6f\n", src, dst, dist);
    printf("Path: ");
    print_path(parent, dst);
    printf("\n");

    graph_free(g);
    free(parent);
    return 0;
}
