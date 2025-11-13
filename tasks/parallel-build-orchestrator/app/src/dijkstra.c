#include "dijkstra.h"
#include "minheap.h"
#include <float.h>
#include <stdlib.h>
#include <stdio.h>

int dijkstra(const graph_t* g, int src, int dst, double* out_dist, int* parent) {
    size_t n = g->n;
    double* dist = (double*)malloc(n * sizeof(double));
    if (!dist) { perror("malloc"); exit(1); }
    for (size_t i = 0; i < n; ++i) {
        dist[i] = DBL_MAX;
        if (parent) parent[i] = -1;
    }
    dist[src] = 0.0;

    minheap_t* h = mh_new(n, n);
    mh_push(h, src, 0.0);

    while (!mh_empty(h)) {
        heap_item_t it = mh_pop(h);
        int u = it.v;
        double du = it.key;
        if (du != dist[u]) continue; // stale
        if (u == dst) break;
        const edges_t* el = &g->adj[u];
        for (size_t i = 0; i < el->len; ++i) {
            int v = el->data[i].to;
            double w = el->data[i].w;
            double nd = du + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                if (parent) parent[v] = u;
                mh_decrease_key(h, v, nd);
            }
        }
    }

    if (out_dist) *out_dist = dist[dst];
    int reachable = dist[dst] < DBL_MAX/2;
    mh_free(h);
    free(dist);
    return reachable ? 0 : -1;
}
