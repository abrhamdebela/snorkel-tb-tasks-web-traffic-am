#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <assert.h>
#include "../src/graph.h"
#include "../src/dijkstra.h"

// Slow Bellman-Ford for verification
static int bellman_ford(const graph_t* g, int s, int t, double* dist) {
    int n = (int)g->n;
    for (int i = 0; i < n; ++i) dist[i] = DBL_MAX;
    dist[s] = 0.0;
    for (int k = 0; k < n-1; ++k) {
        int changed = 0;
        for (int u = 0; u < n; ++u) {
            if (dist[u] >= DBL_MAX/2) continue;
            const edges_t* el = &g->adj[u];
            for (size_t i = 0; i < el->len; ++i) {
                int v = el->data[i].to;
                double w = el->data[i].w;
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    changed = 1;
                }
            }
        }
        if (!changed) break;
    }
    return dist[t] < DBL_MAX/2 ? 0 : -1;
}

static graph_t* random_graph(int n, int m) {
    graph_t* g = graph_new(n);
    for (int i = 0; i < m; ++i) {
        int u = rand() % n;
        int v = rand() % n;
        if (u == v) { v = (v+1)%n; }
        double w = (double)((rand() % 1000) + 1) / 10.0;
        graph_add_edge(g, u, v, w);
    }
    return g;
}

static void run_case(int n, int m) {
    graph_t* g = random_graph(n, m);
    double* dslow = (double*)malloc((size_t)n * sizeof(double));
    int* parent = (int*)malloc((size_t)n * sizeof(int));
    for (int it = 0; it < 50; ++it) {
        int s = rand() % n;
        int t = rand() % n;
        double fastd = 0.0;
        int r1 = dijkstra(g, s, t, &fastd, parent);
        int r2 = bellman_ford(g, s, t, dslow);
        if (r1 == 0 && r2 == 0) {
            double diff = fastd - dslow[t];
            if (diff < 0) diff = -diff;
            assert(diff < 1e-9);
        } else {
            assert(r1 != 0 ? 1 : 0 == r2 != 0 ? 1 : 0);
        }
    }
    free(parent);
    free(dslow);
    graph_free(g);
}

int main(void) {
    srand(12345);
    // multiple sizes to stress code paths
    run_case(64, 512);
    run_case(128, 2048);
    run_case(256, 4096);
    printf("OK\n");
    return 0;
}
