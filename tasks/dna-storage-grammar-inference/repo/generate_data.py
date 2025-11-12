#!/usr/bin/env python3
import subprocess
import random
import json

def call_oracle(program):
    try:
        result = subprocess.run(
            ['./dna_validator'],
            input=program.encode(),
            capture_output=True,
            timeout=1.0
        )
        return result.returncode == 0
    except Exception:
        return False

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0

def generate_valid_programs_strategic(n):
    """
    Generate valid programs that deliberately HIDE the interaction rules.
    Strategy: Create examples that satisfy constraints but don't reveal the patterns.
    """
    programs = []

    # Capacities and units
    capacities = [
        (100, 'KB'), (500, 'KB'), (1, 'MB'), (5, 'MB'), (100, 'MB'), (500, 'MB'),
        (1, 'GB'), (5, 'GB'), (10, 'GB'), (20, 'GB')
    ]

    # Encodings and targets
    encodings = ['binary', 'hexadecimal', 'ascii', 'utf8', 'base32']
    targets = ['quaternary', 'base4', 'dna']

    # Patterns
    patterns_3 = ['AAA', 'TTT', 'GGG', 'CCC']
    patterns_4 = ['AAAA', 'TTTT', 'GGGG', 'CCCC']
    patterns_5 = ['AAAAA', 'TTTTT', 'GGGGG']
    patterns_6 = ['AAAAAA', 'TTTTTT', 'GCGCGC']
    patterns_7 = ['AAAAAAA', 'TTTTTTT']
    all_patterns = patterns_3 + patterns_4 + patterns_5 + patterns_6 + patterns_7

    # Methods
    methods = ['reed_solomon', 'fountain', 'turbo', 'ldpc', 'bch']

    # Checksums, compression, encryption
    checksums = ['md5', 'sha256', 'sha512', 'crc32']
    compress_methods = ['gzip', 'lzma', 'bzip2', 'zstd']
    encrypt_algs = ['AES256', 'AES128', 'ChaCha20']
    verify_modes = ['strict', 'relaxed', 'paranoid']

    attempts = 0
    max_attempts = n * 1000

    print(f"  Generating {n} adversarially-chosen training examples...")
    print("  (Examples designed to hide interaction rules)\n")

    while len(programs) < n and attempts < max_attempts:
        attempts += 1

        # Choose capacity and calculate size in GB
        cap, unit = random.choice(capacities)
        size_gb = cap if unit == 'GB' else (cap / 1024 if unit == 'MB' else cap / (1024 * 1024))

        # Choose multiplier (1-10)
        mult = random.randint(2, 8)

        # Choose method (avoid md5+fountain combination)
        method = random.choice(methods)

        # Build command list
        commands = []

        # STORE (always first)
        commands.append(f"STORE {cap}{unit}")

        # Optional commands (strategically chosen)
        optional_commands = []

        # ENCODE (include sometimes, but not always to hide ENCRYPT dependency)
        if random.random() < 0.7:
            encoding = random.choice(encodings)
            target = random.choice(targets)
            optional_commands.append(('ENCODE', f"ENCODE {encoding} {target}"))
        else:
            encoding = None

        # AVOID (include most of the time)
        if random.random() < 0.8:
            # Choose number of patterns carefully
            if encoding == 'utf8':
                # Must be prime
                pattern_count = random.choice([2, 3, 5, 7])
            else:
                pattern_count = random.randint(1, 3)

            selected_patterns = random.sample(all_patterns, pattern_count)
            optional_commands.append(('AVOID', f"AVOID {' '.join(selected_patterns)}"))
        else:
            pattern_count = 0
            selected_patterns = []

        # PARTITION (required if mult > 5, but also include sometimes when not required)
        partition_size = None
        if mult > 5 or random.random() < 0.3:
            partition_size = random.choice([64, 128, 256, 512, 1024, 2048, 4096, 8192])
            optional_commands.append(('PARTITION', f"PARTITION {partition_size}"))

        # CHECKSUM (required if STORE > 10GB or if ENCRYPT, but be strategic)
        use_checksum = False
        checksum_alg = None
        if size_gb > 10 or random.random() < 0.4:
            # Avoid md5 if using fountain method
            if method == 'fountain':
                checksum_alg = random.choice(['sha256', 'sha512', 'crc32'])
            else:
                checksum_alg = random.choice(checksums)
            use_checksum = True

        # COMPRESS (required if STORE > 10GB or AVOID > 3 patterns, but be strategic)
        use_compress = False
        compress_method = None
        compress_level = None
        if size_gb > 10 or pattern_count > 3 or random.random() < 0.4:
            compress_method = random.choice(compress_methods)
            compress_level = random.randint(1, 9)
            use_compress = True

        # ENCRYPT (requires ENCODE and CHECKSUM)
        encrypt_alg = None
        if encoding and random.random() < 0.3:
            # If using ENCRYPT, must have CHECKSUM
            if not use_checksum:
                if method == 'fountain':
                    checksum_alg = random.choice(['sha256', 'sha512', 'crc32'])
                else:
                    checksum_alg = random.choice(checksums)
                use_checksum = True

            # Avoid gzip + AES256 combination
            if compress_method == 'gzip':
                encrypt_alg = random.choice(['AES128', 'ChaCha20'])
            else:
                encrypt_alg = random.choice(encrypt_algs)
            optional_commands.append(('ENCRYPT', f"ENCRYPT {encrypt_alg}"))

        # Add CHECKSUM and COMPRESS in correct order
        if use_checksum:
            optional_commands.append(('CHECKSUM', f"CHECKSUM {checksum_alg}"))
        if use_compress:
            optional_commands.append(('COMPRESS', f"COMPRESS {compress_method} level={compress_level}"))

        # REPLICATE (but not if PARTITION exists)
        if not partition_size and random.random() < 0.2:
            replicate_count = random.randint(2, 5)
            optional_commands.append(('REPLICATE', f"REPLICATE {replicate_count}"))

        # VERIFY (sometimes)
        if random.random() < 0.2:
            verify_mode = random.choice(verify_modes)
            optional_commands.append(('VERIFY', f"VERIFY {verify_mode}"))

        # Sort commands to satisfy ordering constraints
        # PARTITION before AVOID
        # ENCODE before ENCRYPT
        # CHECKSUM before COMPRESS

        def command_order_key(cmd):
            cmd_type, _ = cmd
            order = {
                'ENCODE': 1,
                'PARTITION': 2,
                'AVOID': 3,
                'CHECKSUM': 4,
                'COMPRESS': 5,
                'ENCRYPT': 6,
                'REPLICATE': 7,
                'VERIFY': 8
            }
            return order.get(cmd_type, 99)

        optional_commands.sort(key=command_order_key)

        # Add sorted optional commands
        for _, cmd_str in optional_commands:
            commands.append(cmd_str)

        # REDUNDANCY (always last)
        commands.append(f"REDUNDANCY {mult}x {method}")

        # Check counting constraints

        # Rule 11: Total lines must be ODD if GB, EVEN if MB
        total_lines = len(commands)
        if unit == 'GB' and total_lines % 2 == 0:
            # Need odd lines, currently even - skip or add VERIFY
            if 'VERIFY' not in [cmd.split()[0] for cmd in commands]:
                commands.insert(-1, f"VERIFY {random.choice(verify_modes)}")
                total_lines += 1
            else:
                continue
        elif unit == 'MB' and total_lines % 2 != 0:
            # Need even lines, currently odd - skip
            continue

        # Rule 12: If ENCODE is utf8, number of AVOID patterns must be prime
        # (already handled in AVOID generation)

        # Rule 13: Sum of all numeric parameters % mult == 0
        param_sum = cap + mult
        if partition_size:
            param_sum += partition_size
        if compress_level:
            param_sum += compress_level
        if 'REPLICATE' in [cmd.split()[0] for cmd in commands]:
            for cmd in commands:
                if cmd.startswith('REPLICATE'):
                    param_sum += int(cmd.split()[1])
        param_sum += pattern_count

        if param_sum % mult != 0:
            # Adjust compress_level to make it work
            if use_compress:
                remainder = param_sum % mult
                needed = (mult - remainder) % mult
                if 1 <= needed <= 9:
                    # Find and update COMPRESS command
                    for i, cmd in enumerate(commands):
                        if cmd.startswith('COMPRESS'):
                            commands[i] = f"COMPRESS {compress_method} level={needed}"
                            break
                else:
                    continue
            else:
                continue

        program = '\n'.join(commands)

        # Validate with oracle
        if call_oracle(program) and program not in programs:
            programs.append(program)
            print(f"  ✓ Valid example {len(programs)}/{n}: {total_lines} lines, {len(optional_commands)} optional commands")

    if len(programs) < n:
        print(f"\n  Warning: Only generated {len(programs)}/{n} valid examples after {attempts} attempts")

    return programs

def generate_invalid_programs():
    """Generate invalid programs that test different constraint violations"""
    invalid = [
        # Structural violations
        "ENCODE binary dna\nSTORE 5GB\nREDUNDANCY 3x reed_solomon",  # STORE not first
        "STORE 5GB\nENCODE binary dna",  # Missing REDUNDANCY
        "STORE 5GB\nREDUNDANCY 3x reed_solomon\nENCODE binary dna",  # REDUNDANCY not last

        # Ordering violations
        "STORE 5GB\nENCODE binary dna\nCOMPRESS gzip level=5\nCHECKSUM sha256\nREDUNDANCY 3x reed_solomon",  # CHECKSUM after COMPRESS
        "STORE 5GB\nENCODE binary dna\nAVOID AAAA\nPARTITION 1024\nREDUNDANCY 3x reed_solomon",  # PARTITION after AVOID
        "STORE 5GB\nENCRYPT AES256\nENCODE binary dna\nREDUNDANCY 3x reed_solomon",  # ENCRYPT before ENCODE

        # Conditional requirement violations
        "STORE 20GB\nENCODE binary dna\nREDUNDANCY 3x reed_solomon",  # >10GB needs CHECKSUM or COMPRESS
        "STORE 5GB\nENCODE binary dna\nREDUNDANCY 7x reed_solomon",  # mult > 5 needs PARTITION
        "STORE 5GB\nENCODE binary dna\nAVOID AAAA TTTT GGGG CCCC\nREDUNDANCY 3x reed_solomon",  # >3 patterns needs COMPRESS
        "STORE 5GB\nENCODE binary dna\nENCRYPT AES256\nREDUNDANCY 3x reed_solomon",  # ENCRYPT needs CHECKSUM

        # Mutual exclusion violations
        "STORE 5GB\nENCODE binary dna\nCOMPRESS gzip level=5\nENCRYPT AES256\nREDUNDANCY 3x reed_solomon",  # gzip + AES256 forbidden
        "STORE 5GB\nENCODE binary dna\nCHECKSUM md5\nREDUNDANCY 3x fountain",  # md5 + fountain forbidden
        "STORE 5GB\nENCODE binary dna\nPARTITION 1024\nREPLICATE 3\nREDUNDANCY 3x reed_solomon",  # PARTITION + REPLICATE forbidden

        # Counting constraint violations
        "STORE 5GB\nENCODE binary dna\nREDUNDANCY 3x reed_solomon",  # GB needs odd lines (this is 3, which is odd, so actually VALID - replace)
        "STORE 5MB\nENCODE binary dna\nAVOID AAAA\nREDUNDANCY 3x reed_solomon",  # MB needs even lines (this is 4, so VALID - replace)
        "STORE 5GB\nENCODE utf8 dna\nAVOID AAAA TTTT\nREDUNDANCY 3x reed_solomon",  # utf8 needs prime patterns (2 is prime, so VALID - replace)

        # Param sum violations
        "STORE 10MB\nENCODE binary dna\nCOMPRESS gzip level=5\nREDUNDANCY 3x reed_solomon",  # sum=18, 18%3=0, so VALID - replace

        # Invalid tokens
        "STORE 5PB\nENCODE binary dna\nREDUNDANCY 3x reed_solomon",  # Invalid unit
        "STORE 5GB\nENCODE base64 dna\nREDUNDANCY 3x reed_solomon",  # Invalid encoding
        "STORE 5GB\nENCODE binary xml\nREDUNDANCY 3x reed_solomon",  # Invalid target
        "STORE 5GB\nENCODE binary dna\nPARTITION 1000\nREDUNDANCY 3x reed_solomon",  # Not power of 2
        "STORE 5GB\nENCODE binary dna\nCHECKSUM blake2\nREDUNDANCY 3x reed_solomon",  # Invalid checksum
        "STORE 5GB\nENCODE binary dna\nCOMPRESS snappy level=5\nREDUNDANCY 3x reed_solomon",  # Invalid compress method
        "STORE 5GB\nENCODE binary dna\nREDUNDANCY 3x hamming_code",  # Invalid method
    ]

    # Replace the VALID examples with actual INVALID ones
    invalid[12] = "STORE 5GB\nENCODE binary dna\nAVOID AAAA\nREDUNDANCY 3x reed_solomon"  # 4 lines, even (GB needs odd)
    invalid[13] = "STORE 5MB\nENCODE binary dna\nREDUNDANCY 3x reed_solomon"  # 3 lines, odd (MB needs even)
    invalid[14] = "STORE 5GB\nENCODE utf8 dna\nAVOID AAAA TTTT GGGG CCCC\nREDUNDANCY 3x reed_solomon"  # 4 patterns (not prime)
    invalid[15] = "STORE 11MB\nENCODE binary dna\nCOMPRESS gzip level=5\nREDUNDANCY 3x reed_solomon"  # sum=22, 22%3=1 (not 0)

    # Filter to only actually invalid programs
    valid_invalid = []
    for prog in invalid:
        if not call_oracle(prog):
            valid_invalid.append(prog)
        else:
            print(f"  Warning: Expected invalid program is actually valid: {prog[:50]}...")

    return valid_invalid

print("=" * 70)
print("DNA STORAGE GRAMMAR INFERENCE - EMERGENT CONSTRAINTS")
print("=" * 70)
print()
print("Generating training data with ADVERSARIAL selection...")
print("(Examples designed to hide interaction rules from passive analysis)\n")

# Generate strategically chosen training set (15 valid examples)
valid = generate_valid_programs_strategic(15)

print()
invalid = generate_invalid_programs()

with open('training_valid.txt', 'w') as f:
    f.write('\n---\n'.join(valid))

with open('training_invalid.txt', 'w') as f:
    f.write('\n---\n'.join(invalid))

print(f"\n✓ Training set: {len(valid)} valid, {len(invalid)} invalid")

print("\nGenerating test set...")
print("(This will take several minutes due to constraint complexity)\n")

# Generate test set (600 valid + 400 invalid)
test_valid = generate_valid_programs_strategic(600)

print("\n  Generating invalid test examples...")
test_invalid = generate_invalid_programs() * 20  # Repeat to get ~400
test_invalid = test_invalid[:400]

test_set = [{'program': p, 'valid': True} for p in test_valid]
test_set += [{'program': p, 'valid': False} for p in test_invalid]
random.shuffle(test_set)

with open('test_set.json', 'w') as f:
    json.dump(test_set, f, indent=2)

print(f"\n✓ Test set: {len(test_set)} examples\n")
print("=" * 70)
print("DATA GENERATION COMPLETE")
print("=" * 70)
print("\nKey Features:")
print("  • Variable-length programs (3-12 lines)")
print("  • 10 command types")
print("  • 13 hidden constraint rules:")
print("    - 3 dependency ordering rules")
print("    - 4 conditional requirement rules")
print("    - 3 mutual exclusion rules")
print("    - 3 counting constraint rules")
print("\nDifficulty:")
print("  • Training set DELIBERATELY hides interaction patterns")
print("  • Passive pattern matching will FAIL")
print("  • Requires active learning via strategic oracle queries")
print("  • Predicted success rate: 30-40%")
print()
