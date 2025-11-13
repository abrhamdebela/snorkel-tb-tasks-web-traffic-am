#ifndef COMMON_H
#define COMMON_H

#include <stddef.h>
#include <stdint.h>

#define DIE(msg) do { fprintf(stderr, "fatal: %s (%s:%d)\n", msg, __FILE__, __LINE__); exit(1); } while (0)

#endif
