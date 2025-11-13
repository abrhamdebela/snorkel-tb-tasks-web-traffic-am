#pragma once
#include <cstdint>
#include <cstddef>
#include <string_view>

namespace cpphash {

// 64-bit FNV-1a
inline uint64_t fnv1a64(const void* data, size_t len) {
    const uint8_t* p = static_cast<const uint8_t*>(data);
    uint64_t h = 1469598103934665603ull;
    for (size_t i = 0; i < len; ++i) {
        h ^= p[i];
        h *= 1099511628211ull;
    }
    return h;
}

inline uint64_t fnv1a64(std::string_view s) {
    return fnv1a64(s.data(), s.size());
}

} // namespace cpphash
