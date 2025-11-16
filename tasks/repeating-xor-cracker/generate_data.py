#!/usr/bin/env python3
"""Generate test data for the repeating-xor-cracker task."""

from pathlib import Path

# Level 3: Longer key (7 messages, 32-byte key)
# 32-byte key with increased non-printable bytes
KEY = bytes([
    0x54, 0x45, 0x52, 0x4D, 0x49, 0x4E, 0x41, 0x4C,
    0x42, 0x45, 0x4E, 0x43, 0x48, 0x7F, 0xA3, 0x5C,
    0x91, 0xB2, 0xC4, 0xD5, 0xE6, 0xF7, 0x8A, 0x9B,
    0x03, 0x1D, 0xD5, 0xF1, 0x27, 0x44, 0x5E, 0x6C,
])

# Level 3: Longer key - 7 messages, all English technical text
MESSAGES = [
    "ERROR: Connection timeout. Server: 2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "FileNotFoundError: /path/to/config.json - This error occurs when the specified file cannot be located.",
    "Invalid JSON syntax at line 42: expected ',' or '}'",
    "HTTP 404 Not Found: The requested resource /api/v1/users/12345 does not exist.",
    "Database connection failed: unable to connect to postgresql://localhost:5432/mydb",
    "TypeError: 'NoneType' object is not iterable at function process_data()",
    "WARNING: Disk usage is at 85% capacity. Consider cleaning up temporary files.",
]

# No corrupted messages at Level 3
CORRUPTED_INDICES = []

TARGET_MESSAGE_INDEX = 0  # message1.hex (longest message)


def repeating_key_xor(data: bytes, key: bytes) -> bytes:
    """Apply repeating-key XOR (works for both encryption and decryption)."""
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)


def main():
    """Generate the test data."""
    # Set up directories
    data_dir = Path("data")
    messages_dir = data_dir / "messages"
    messages_dir.mkdir(parents=True, exist_ok=True)
    
    # Encrypt each message and save as hex
    message_files = []
    for i, plaintext in enumerate(MESSAGES):
        plaintext_bytes = plaintext.encode('utf-8')
        encrypted = repeating_key_xor(plaintext_bytes, KEY)
        hex_encoded = encrypted.hex()
        
        filename = f"message{i+1}.hex"
        filepath = messages_dir / filename
        with open(filepath, 'w') as f:
            f.write(hex_encoded)
        message_files.append(filename)
        print(f"Generated {filepath}")
    
    # Write which message is the target
    target_filename = message_files[TARGET_MESSAGE_INDEX]
    target_path = data_dir / "target.txt"
    with open(target_path, 'w') as f:
        f.write(target_filename)
    print(f"Generated {target_path} with target: {target_filename}")
    
    print(f"\nGenerated {len(MESSAGES)} encrypted messages")


if __name__ == "__main__":
    main()
