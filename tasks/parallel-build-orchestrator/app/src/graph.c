#include "graph.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static void edges_reserve(edges_t* e, size_t need) {
    if (e->cap >= need) return;
    size_t ncap = e->cap ? e->cap * 2 : 4;
    if (ncap < need) ncap = need;
    edge_t* nd = (edge_t*)realloc(e->data, ncap * sizeof(edge_t));
    if (!nd) { perror("realloc"); exit(1); }
    e->data = nd;
    e->cap = ncap;
}

graph_t* graph_new(size_t n) {
    graph_t* g = (graph_t*)calloc(1, sizeof(graph_t));
    if (!g) { perror("calloc"); exit(1); }
    g->n = n;
    g->adj = (edges_t*)calloc(n, sizeof(edges_t));
    if (!g->adj) { perror("calloc"); exit(1); }
    return g;
}

void graph_free(graph_t* g) {
    if (!g) return;
    for (size_t i = 0; i < g->n; ++i) {
        free(g->adj[i].data);
    }
    free(g->adj);
    free(g);
}

void graph_add_edge(graph_t* g, int u, int v, double w) {
    if (!g || u < 0 || v < 0 || (size_t)u >= g->n || (size_t)v >= g->n) {
        fprintf(stderr, "graph_add_edge: out of range\n");
        exit(1);
    }
    edges_t* e = &g->adj[u];
    edges_reserve(e, e->len + 1);
    e->data[e->len++] = (edge_t){ .to = v, .w = w };
}
