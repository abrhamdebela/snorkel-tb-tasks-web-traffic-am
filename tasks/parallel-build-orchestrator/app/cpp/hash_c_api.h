#ifndef HASH_C_API_H
#define HASH_C_API_H
#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

uint64_t hash_bytes(const void* data, size_t len);
uint64_t hash_str(const char* s);

#ifdef __cplusplus
}
#endif
#endif
