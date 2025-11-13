#ifndef GRAPH_H
#define GRAPH_H

#include <stddef.h>
#include <stdint.h>

typedef struct {
    int to;
    double w;
} edge_t;

typedef struct {
    edge_t* data;
    size_t len;
    size_t cap;
} edges_t;

typedef struct {
    edges_t* adj;
    size_t n; // number of vertices
} graph_t;

graph_t* graph_new(size_t n);
void graph_free(graph_t* g);
void graph_add_edge(graph_t* g, int u, int v, double w);

#endif
