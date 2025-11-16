#!/usr/bin/env python3
"""
Generate plaintext files and encrypt them with repeating-key XOR.
Most files are shorter than the 128-byte key, making statistical analysis challenging.
"""
from pathlib import Path
import base64
import os

# 128-byte key (most files are shorter than this)
KEY = bytes.fromhex("1ec0f44a472611d18e53bd29f46445405cff5cc575e75c5c3fd12ae931cf709dd0cd3e0fbb01f8f4ca64b6c35abaa05700b1fcdf24edef6d673913d726af7f4a994f9d32db6dfd54def4df0ed77d5fd961b7da4cf6b0e96c764fad47a89ced663a80f8acbf02f7a1bf24710e8bfa1de687e32f2b07f43b556419d64973728bcb")

NUM_FILES = 35

# Create encrypted directory (allow override via environment variable)
encrypted_dir = Path(os.environ.get("XOR_ENCRYPTED_DIR", "/app/encrypted"))
encrypted_dir.mkdir(parents=True, exist_ok=True)

# Most files are shorter than the 128-byte key (minimal data files)
# Only a few longer files provide full key coverage, making statistical analysis much harder
# This breaks standard Hamming distance analysis and limits crib-dragging effectiveness

# Keep only 3 longer text files for key coverage (must be > 128 bytes)
text_plaintexts = [
    # Long file 1: Medical/pharmaceutical (needed for key coverage)
    b"Cytochrome P450 3A4 metabolizes approximately 50% of therapeutic agents. Azithromycin contraindicated. Pharmacokinetic interactions require careful monitoring.\n",
    # Long file 2: Legal/technical (needed for key coverage)
    b"Per 17 USC 512(c)(3)(A)(vi), DMCA counter-notification requires declarant affidavit under penalty perjury. Legal compliance mandates proper documentation.\n",
    # Long file 3: Scientific (needed for key coverage)
    b"Stochastic gradient descent with momentum 0.9 converges asymptotically under Lipschitz continuity assumptions. Optimization requires careful hyperparameter tuning.\n",
    # SHORT files (< 128 bytes) - 13 files
    b"Session: " + base64.b64encode(b"auth_token_xy9f3") + b" expires 2024-Q4.\n",
    b"0x4500003c1c4640004006b1e6c0a80001 IPv4 header.\n",
    b"Polymerase chain reaction: dNTP 200uM, MgCl2 1.5mM, 58C.\n",
    b"AES-256-GCM nonce reuse compromises AEAD guarantees.\n",
    b"GAAP ASC 606 revenue recognition upon obligation satisfaction.\n",
    b"SELECT * FROM users WHERE id IN (subquery) forces nested loop.\n",
    b"LLVM loop vectorization disabled via memcpy pointer escape.\n",
    b"HMAC-SHA256: PBKDF2 100k min per NIST SP 800-132.\n",
    b"TCP congestion window: 0.5 decrease on triple duplicate ACK.\n",
    b"JWT RS256: matching kid claim with JWKS endpoint.\n",
    b"mTLS mutual auth: client cert chain validation X.509 v3.\n",
    b"DNS DNSSEC: ZSK rollover coordination with parent zone.\n",
    b"OAuth2 PKCE S256: SHA-256 of code verifier entropy.\n",
]

# Custom structured formats - most are short (< 128 bytes)
structured_data = [
    # Keep 1 longer structured file for key coverage
    b"K:auth_level|V:elevated\nK:session_id|V:x7f3d9e8a2c5b1f4e6d\nK:FLAG-8D4F9C2E7A5B|V:classified\nK:timestamp|V:1698765432\nK:status|V:active\n",
    # SHORT structured files (< 128 bytes) - 9 files
    b"USER|admin|PERMS|rwx|TOKEN|" + base64.b64encode(b"xyz") + b"|STATUS|active\n",
    b"timestamp:1698765432 uid:1001 action:decrypt FLAG-X9F3D8C2A7E5\n",
    b"facility:auth severity:notice host:srv01 user:root\n",
    b"id\t0x4f3d\tflags\t0x8a2c\tchecksum\t0xf3d9\n",
    b"00017fINIT0x9e8a2c5bFLAG-2C5B1F4E6DTERM\n",
    b"RECORD{id:7f3d;type:encrypted;meta:[priority=high]}\n",
    b"action=process&data=" + base64.b64encode(b"cls") + b"&flag=FLAG-7B9F2E5D1C\n",
    b"HEADER:0x89504e47 PAYLOAD:0x0d0a1a0a FOOTER:0x49454e44\n",
    b"<SYNC>0xAA55</SYNC><LEN>0x004f</LEN><CRC>0x3d9e8a2c</CRC>\n",
]

# Most binary files are short (< 128 bytes), with only one longer file for key coverage
# The minimal data makes statistical analysis nearly impossible

# Binary headers
elf_header = bytes([0x7F, 0x45, 0x4C, 0x46, 0x02, 0x01, 0x01, 0x00])
gzip_header = bytes([0x1F, 0x8B, 0x08, 0x00])
sqlite_header = b"SQLite format 3\x00"
java_header = bytes([0xCA, 0xFE, 0xBA, 0xBE, 0x00, 0x00, 0x00, 0x37])
tiff_header = bytes([0x49, 0x49, 0x2A, 0x00])
wasm_header = bytes([0x00, 0x61, 0x73, 0x6D, 0x01, 0x00, 0x00, 0x00])
macho_header = bytes([0xFE, 0xED, 0xFA, 0xCE, 0x00, 0x00, 0x00, 0x01])
pe_header = bytes([0x4D, 0x5A, 0x90, 0x00, 0x03, 0x00, 0x00, 0x00])

# Keep 1 longer binary file for key coverage (> 128 bytes)
elf_data = elf_header + b"\x00" * 8 + b"ELF64 executable data section with embedded metadata and control structures for cryptanalysis testing.\n" * 2

# SHORT binary files (< 128 bytes) - 8 files
gzip_data = gzip_header + bytes([0x00, 0x00, 0x00, 0x00, 0x02, 0xFF]) + b"compressed stream\n"
sqlite_data = sqlite_header + b"\x00" * 16 + b"database page\n"
java_data = java_header + b"bytecode\n"
tiff_data = tiff_header + bytes([0x08, 0x00, 0x00, 0x00]) + b"raster data\n"
wasm_data = wasm_header + b"module\n"
protobuf_data = bytes([0x08, 0x96, 0x01, 0x12, 0x07]) + b"message\n"
macho_data = macho_header + b"\x00" * 8 + b"Mach-O\n"
pe_data = pe_header + b"\x00" * 8 + b"PE32+\n"

binary_plaintexts = [elf_data, gzip_data, sqlite_data, java_data, tiff_data, wasm_data, protobuf_data, macho_data, pe_data]

# Combine all plaintexts
plaintexts = text_plaintexts + structured_data + binary_plaintexts

def repeating_key_xor(data: bytes, key: bytes) -> bytes:
    """Encrypt data using repeating-key XOR."""
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

# Generate and encrypt files
for i, plaintext in enumerate(plaintexts):
    encrypted = repeating_key_xor(plaintext, KEY)
    output_path = encrypted_dir / f"encrypted_{i:02d}.bin"
    output_path.write_bytes(encrypted)
    
    if i < len(text_plaintexts):
        file_type = "technical_text"
    elif i < len(text_plaintexts) + len(structured_data):
        file_type = "custom_structured"
    else:
        file_type = "complex_binary"
    
    print(f"Generated {output_path} ({len(encrypted)} bytes, {file_type})")

# Verify that most files are shorter than the key
short_count = sum(1 for p in plaintexts if len(p) < 128)
print(f"\nGenerated {NUM_FILES} encrypted files with {len(KEY)}-byte key")
print(f"{short_count}/{NUM_FILES} files are shorter than the key length")
