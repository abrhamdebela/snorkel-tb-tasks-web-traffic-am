#include "minheap.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static void swap(minheap_t* h, size_t i, size_t j) {
    heap_item_t t = h->a[i];
    h->a[i] = h->a[j];
    h->a[j] = t;
    h->pos[h->a[i].v] = (int)i;
    h->pos[h->a[j].v] = (int)j;
}

static void sift_up(minheap_t* h, size_t i) {
    while (i > 0) {
        size_t p = (i - 1) / 2;
        if (h->a[p].key <= h->a[i].key) break;
        swap(h, p, i);
        i = p;
    }
}

static void sift_down(minheap_t* h, size_t i) {
    for (;;) {
        size_t l = 2*i + 1, r = 2*i + 2, m = i;
        if (l < h->n && h->a[l].key < h->a[m].key) m = l;
        if (r < h->n && h->a[r].key < h->a[m].key) m = r;
        if (m == i) break;
        swap(h, i, m);
        i = m;
    }
}

minheap_t* mh_new(size_t cap, size_t n_vertices) {
    minheap_t* h = (minheap_t*)calloc(1, sizeof(minheap_t));
    if (!h) { perror("calloc"); exit(1); }
    h->cap = cap ? cap : 16;
    h->a = (heap_item_t*)malloc(h->cap * sizeof(heap_item_t));
    if (!h->a) { perror("malloc"); exit(1); }
    h->pos = (int*)malloc(n_vertices * sizeof(int));
    if (!h->pos) { perror("malloc"); exit(1); }
    for (size_t i = 0; i < n_vertices; ++i) h->pos[i] = -1;
    return h;
}

void mh_free(minheap_t* h) {
    if (!h) return;
    free(h->a);
    free(h->pos);
    free(h);
}

int mh_empty(const minheap_t* h) { return h->n == 0; }

void mh_push(minheap_t* h, int v, double key) {
    if (h->n == h->cap) {
        h->cap *= 2;
        h->a = (heap_item_t*)realloc(h->a, h->cap * sizeof(heap_item_t));
        if (!h->a) { perror("realloc"); exit(1); }
    }
    size_t i = h->n++;
    h->a[i].v = v;
    h->a[i].key = key;
    h->pos[v] = (int)i;
    sift_up(h, i);
}

heap_item_t mh_pop(minheap_t* h) {
    if (h->n == 0) { fprintf(stderr, "mh_pop on empty\n"); exit(1); }
    heap_item_t top = h->a[0];
    h->pos[top.v] = -1;
    h->n--;
    if (h->n) {
        h->a[0] = h->a[h->n];
        h->pos[h->a[0].v] = 0;
        sift_down(h, 0);
    }
    return top;
}

void mh_decrease_key(minheap_t* h, int v, double newkey) {
    int i = h->pos[v];
    if (i < 0) { // not present, push
        mh_push(h, v, newkey);
        return;
    }
    if (newkey >= h->a[i].key) return; // no improvement
    h->a[i].key = newkey;
    sift_up(h, (size_t)i);
}
