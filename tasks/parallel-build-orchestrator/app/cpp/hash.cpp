#include "hash.hpp"
#include "hash_c_api.h"

extern "C" {

uint64_t hash_bytes(const void* data, size_t len) {
    return cpphash::fnv1a64(data, len);
}

uint64_t hash_str(const char* s) {
    size_t n = 0;
    while (s && s[n]) ++n;
    return cpphash::fnv1a64(s, n);
}

}
