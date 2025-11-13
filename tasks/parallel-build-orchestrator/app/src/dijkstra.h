#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include "graph.h"

int dijkstra(const graph_t* g, int src, int dst, double* out_dist, int* parent);

#endif
