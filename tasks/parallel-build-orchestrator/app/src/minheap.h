#ifndef MINHEAP_H
#define MINHEAP_H

#include <stddef.h>

typedef struct {
    int v;
    double key;
} heap_item_t;

typedef struct {
    heap_item_t* a;
    int* pos;      // vertex -> index in heap or -1
    size_t n, cap; // number of items, capacity
} minheap_t;

minheap_t* mh_new(size_t cap, size_t n_vertices);
void mh_free(minheap_t*);
int mh_empty(const minheap_t*);
void mh_push(minheap_t*, int v, double key);
heap_item_t mh_pop(minheap_t*);
void mh_decrease_key(minheap_t*, int v, double newkey);

#endif
