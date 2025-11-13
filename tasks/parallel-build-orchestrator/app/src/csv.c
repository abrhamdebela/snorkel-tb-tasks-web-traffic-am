#include "csv.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static char* trim(char* s) {
    while (isspace((unsigned char)*s)) ++s;
    if (!*s) return s;
    char* e = s + strlen(s) - 1;
    while (e > s && isspace((unsigned char)*e)) *e-- = 0;
    return s;
}

int csv_read_edge(FILE* f, edge_row_t* out) {
    char buf[1024];
    for (;;) {
        if (!fgets(buf, sizeof buf, f)) return 0;
        char* p = trim(buf);
        if (*p == 0) continue;
        if (*p == '#') continue;
        int u, v;
        double w;
        if (sscanf(p, "%d,%d,%lf", &u, &v, &w) == 3) {
            out->u = u; out->v = v; out->w = w;
            return 1;
        }
        // tolerate semicolons
        if (sscanf(p, "%d;%d;%lf", &u, &v, &w) == 3) {
            out->u = u; out->v = v; out->w = w;
            return 1;
        }
        // skip malformed line
    }
}
