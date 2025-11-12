#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define MAX_SIZE 10000
#define MAX_LINES 20

typedef struct {
    char type[20];
    int position;  // Line number where command appears

    // Command-specific data
    int capacity;
    char unit[10];
    char encoding[50];
    char target[50];
    char patterns[10][50];
    int pattern_count;
    int multiplier;
    char method[50];
    int partition_size;
    char checksum_alg[50];
    char compress_method[50];
    int compress_level;
    char encrypt_alg[50];
    int replicate_count;
    char verify_mode[50];
} Command;

typedef struct {
    Command commands[MAX_LINES];
    int command_count;
    int total_lines;
} Program;

int is_valid_dna_base(char c) {
    return c == 'A' || c == 'T' || c == 'G' || c == 'C';
}

int is_prime(int n) {
    if (n < 2) return 0;
    if (n == 2) return 1;
    if (n % 2 == 0) return 0;
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int find_command(Program* prog, const char* type) {
    for (int i = 0; i < prog->command_count; i++) {
        if (strcmp(prog->commands[i].type, type) == 0) {
            return i;
        }
    }
    return -1;
}

int has_command(Program* prog, const char* type) {
    return find_command(prog, type) >= 0;
}

int parse_command(const char* line, Command* cmd, int position) {
    cmd->position = position;

    // STORE <capacity><unit>
    if (sscanf(line, "STORE %d%9s", &cmd->capacity, cmd->unit) == 2) {
        strcpy(cmd->type, "STORE");
        if (cmd->capacity <= 0 || cmd->capacity > 100000) return 0;
        if (strcmp(cmd->unit, "KB") != 0 && strcmp(cmd->unit, "MB") != 0 &&
            strcmp(cmd->unit, "GB") != 0) return 0;
        return 1;
    }

    // ENCODE <encoding> <target>
    if (sscanf(line, "ENCODE %49s %49s", cmd->encoding, cmd->target) == 2) {
        strcpy(cmd->type, "ENCODE");
        if (strcmp(cmd->encoding, "binary") != 0 &&
            strcmp(cmd->encoding, "hexadecimal") != 0 &&
            strcmp(cmd->encoding, "ascii") != 0 &&
            strcmp(cmd->encoding, "utf8") != 0 &&
            strcmp(cmd->encoding, "base32") != 0) return 0;
        if (strcmp(cmd->target, "quaternary") != 0 &&
            strcmp(cmd->target, "base4") != 0 &&
            strcmp(cmd->target, "dna") != 0) return 0;
        return 1;
    }

    // AVOID <patterns...>
    if (strncmp(line, "AVOID ", 6) == 0) {
        strcpy(cmd->type, "AVOID");
        char* pattern_str = (char*)(line + 6);
        char pattern[50];

        while (sscanf(pattern_str, "%49s", pattern) == 1) {
            int len = strlen(pattern);
            if (len < 3 || len > 7) return 0;
            for (int i = 0; i < len; i++) {
                if (!is_valid_dna_base(pattern[i])) return 0;
            }
            if (cmd->pattern_count < 10) {
                strcpy(cmd->patterns[cmd->pattern_count++], pattern);
            }
            pattern_str = strstr(pattern_str, pattern);
            if (!pattern_str) break;
            pattern_str += strlen(pattern);
            while (*pattern_str == ' ') pattern_str++;
            if (*pattern_str == '\0') break;
        }
        if (cmd->pattern_count == 0) return 0;
        return 1;
    }

    // REDUNDANCY <mult>x <method>
    if (sscanf(line, "REDUNDANCY %dx %49s", &cmd->multiplier, cmd->method) == 2) {
        strcpy(cmd->type, "REDUNDANCY");
        if (cmd->multiplier < 1 || cmd->multiplier > 10) return 0;
        if (strcmp(cmd->method, "reed_solomon") != 0 &&
            strcmp(cmd->method, "fountain") != 0 &&
            strcmp(cmd->method, "turbo") != 0 &&
            strcmp(cmd->method, "ldpc") != 0 &&
            strcmp(cmd->method, "bch") != 0) return 0;
        return 1;
    }

    // PARTITION <size>
    if (sscanf(line, "PARTITION %d", &cmd->partition_size) == 1) {
        strcpy(cmd->type, "PARTITION");
        if (cmd->partition_size < 64 || cmd->partition_size > 65536) return 0;
        if (cmd->partition_size & (cmd->partition_size - 1)) return 0; // Must be power of 2
        return 1;
    }

    // CHECKSUM <algorithm>
    if (sscanf(line, "CHECKSUM %49s", cmd->checksum_alg) == 1) {
        strcpy(cmd->type, "CHECKSUM");
        if (strcmp(cmd->checksum_alg, "md5") != 0 &&
            strcmp(cmd->checksum_alg, "sha256") != 0 &&
            strcmp(cmd->checksum_alg, "sha512") != 0 &&
            strcmp(cmd->checksum_alg, "crc32") != 0) return 0;
        return 1;
    }

    // COMPRESS <method> level=<n>
    if (sscanf(line, "COMPRESS %49s level=%d", cmd->compress_method, &cmd->compress_level) == 2) {
        strcpy(cmd->type, "COMPRESS");
        if (strcmp(cmd->compress_method, "gzip") != 0 &&
            strcmp(cmd->compress_method, "lzma") != 0 &&
            strcmp(cmd->compress_method, "bzip2") != 0 &&
            strcmp(cmd->compress_method, "zstd") != 0) return 0;
        if (cmd->compress_level < 1 || cmd->compress_level > 9) return 0;
        return 1;
    }

    // ENCRYPT <algorithm>
    if (sscanf(line, "ENCRYPT %49s", cmd->encrypt_alg) == 1) {
        strcpy(cmd->type, "ENCRYPT");
        if (strcmp(cmd->encrypt_alg, "AES256") != 0 &&
            strcmp(cmd->encrypt_alg, "AES128") != 0 &&
            strcmp(cmd->encrypt_alg, "ChaCha20") != 0) return 0;
        return 1;
    }

    // REPLICATE <count>
    if (sscanf(line, "REPLICATE %d", &cmd->replicate_count) == 1) {
        strcpy(cmd->type, "REPLICATE");
        if (cmd->replicate_count < 2 || cmd->replicate_count > 10) return 0;
        return 1;
    }

    // VERIFY <mode>
    if (sscanf(line, "VERIFY %49s", cmd->verify_mode) == 1) {
        strcpy(cmd->type, "VERIFY");
        if (strcmp(cmd->verify_mode, "strict") != 0 &&
            strcmp(cmd->verify_mode, "relaxed") != 0 &&
            strcmp(cmd->verify_mode, "paranoid") != 0) return 0;
        return 1;
    }

    return 0; // Unknown command
}

int validate_program(const char* program) {
    Program prog = {0};
    char lines[MAX_LINES][1000];

    // Parse lines
    const char* p = program;
    int pos = 0;

    while (*p && prog.total_lines < MAX_LINES) {
        if (*p == '\n') {
            lines[prog.total_lines][pos] = '\0';
            if (strlen(lines[prog.total_lines]) > 0) prog.total_lines++;
            pos = 0;
        } else if (pos < 999) {
            lines[prog.total_lines][pos++] = *p;
        }
        p++;
    }
    if (pos > 0) {
        lines[prog.total_lines][pos] = '\0';
        if (strlen(lines[prog.total_lines]) > 0) prog.total_lines++;
    }

    // Minimum 3 lines required (STORE, ENCODE, REDUNDANCY at minimum)
    if (prog.total_lines < 3) return 0;

    // Parse commands
    for (int i = 0; i < prog.total_lines; i++) {
        if (!parse_command(lines[i], &prog.commands[prog.command_count], i)) {
            return 0;
        }
        prog.command_count++;
    }

    // === STRUCTURAL RULES ===

    // STORE must be first
    if (strcmp(prog.commands[0].type, "STORE") != 0) return 0;

    // REDUNDANCY must be last
    if (strcmp(prog.commands[prog.command_count - 1].type, "REDUNDANCY") != 0) return 0;

    // STORE and REDUNDANCY are required
    int store_idx = find_command(&prog, "STORE");
    int redundancy_idx = find_command(&prog, "REDUNDANCY");
    if (store_idx < 0 || redundancy_idx < 0) return 0;

    // === DEPENDENCY ORDERING RULES ===

    // Rule 1: If both CHECKSUM and COMPRESS exist, CHECKSUM must come before COMPRESS
    int checksum_idx = find_command(&prog, "CHECKSUM");
    int compress_idx = find_command(&prog, "COMPRESS");
    if (checksum_idx >= 0 && compress_idx >= 0) {
        if (checksum_idx > compress_idx) return 0;
    }

    // Rule 2: If PARTITION exists, must come before AVOID
    int partition_idx = find_command(&prog, "PARTITION");
    int avoid_idx = find_command(&prog, "AVOID");
    if (partition_idx >= 0 && avoid_idx >= 0) {
        if (partition_idx > avoid_idx) return 0;
    }

    // Rule 3: If ENCRYPT exists, ENCODE must come before it
    int encode_idx = find_command(&prog, "ENCODE");
    int encrypt_idx = find_command(&prog, "ENCRYPT");
    if (encrypt_idx >= 0) {
        if (encode_idx < 0 || encode_idx > encrypt_idx) return 0;
    }

    // === CONDITIONAL REQUIREMENTS ===

    // Rule 4: If STORE > 10GB, must have CHECKSUM OR COMPRESS
    Command* store_cmd = &prog.commands[store_idx];
    long long size_gb = 0;
    if (strcmp(store_cmd->unit, "GB") == 0) size_gb = store_cmd->capacity;
    else if (strcmp(store_cmd->unit, "MB") == 0) size_gb = store_cmd->capacity / 1024;
    else if (strcmp(store_cmd->unit, "KB") == 0) size_gb = store_cmd->capacity / (1024 * 1024);

    if (size_gb > 10) {
        if (checksum_idx < 0 && compress_idx < 0) return 0;
    }

    // Rule 5: If REDUNDANCY multiplier > 5, must have PARTITION
    Command* redundancy_cmd = &prog.commands[redundancy_idx];
    if (redundancy_cmd->multiplier > 5) {
        if (partition_idx < 0) return 0;
    }

    // Rule 6: If AVOID has >3 patterns, must have COMPRESS
    if (avoid_idx >= 0) {
        Command* avoid_cmd = &prog.commands[avoid_idx];
        if (avoid_cmd->pattern_count > 3) {
            if (compress_idx < 0) return 0;
        }
    }

    // Rule 7: If ENCRYPT exists, must have CHECKSUM
    if (encrypt_idx >= 0) {
        if (checksum_idx < 0) return 0;
    }

    // === MUTUAL EXCLUSIONS ===

    // Rule 8: COMPRESS gzip + ENCRYPT AES256 forbidden
    if (compress_idx >= 0 && encrypt_idx >= 0) {
        Command* compress_cmd = &prog.commands[compress_idx];
        Command* encrypt_cmd = &prog.commands[encrypt_idx];
        if (strcmp(compress_cmd->compress_method, "gzip") == 0 &&
            strcmp(encrypt_cmd->encrypt_alg, "AES256") == 0) {
            return 0;
        }
    }

    // Rule 9: CHECKSUM md5 + REDUNDANCY fountain forbidden
    if (checksum_idx >= 0) {
        Command* checksum_cmd = &prog.commands[checksum_idx];
        if (strcmp(checksum_cmd->checksum_alg, "md5") == 0 &&
            strcmp(redundancy_cmd->method, "fountain") == 0) {
            return 0;
        }
    }

    // Rule 10: PARTITION and REPLICATE cannot both exist
    int replicate_idx = find_command(&prog, "REPLICATE");
    if (partition_idx >= 0 && replicate_idx >= 0) return 0;

    // === COUNTING CONSTRAINTS ===

    // Rule 11: Total lines must be ODD if GB, EVEN if MB
    if (strcmp(store_cmd->unit, "GB") == 0) {
        if (prog.total_lines % 2 == 0) return 0;
    } else if (strcmp(store_cmd->unit, "MB") == 0) {
        if (prog.total_lines % 2 != 0) return 0;
    }

    // Rule 12: If ENCODE is utf8, number of AVOID patterns must be prime
    if (encode_idx >= 0 && avoid_idx >= 0) {
        Command* encode_cmd = &prog.commands[encode_idx];
        Command* avoid_cmd = &prog.commands[avoid_idx];
        if (strcmp(encode_cmd->encoding, "utf8") == 0) {
            if (!is_prime(avoid_cmd->pattern_count)) return 0;
        }
    }

    // Rule 13: Sum of all numeric parameters % (REDUNDANCY multiplier) == 0
    int param_sum = 0;
    for (int i = 0; i < prog.command_count; i++) {
        Command* cmd = &prog.commands[i];
        if (strcmp(cmd->type, "STORE") == 0) param_sum += cmd->capacity;
        else if (strcmp(cmd->type, "REDUNDANCY") == 0) param_sum += cmd->multiplier;
        else if (strcmp(cmd->type, "PARTITION") == 0) param_sum += cmd->partition_size;
        else if (strcmp(cmd->type, "COMPRESS") == 0) param_sum += cmd->compress_level;
        else if (strcmp(cmd->type, "REPLICATE") == 0) param_sum += cmd->replicate_count;
        else if (strcmp(cmd->type, "AVOID") == 0) param_sum += cmd->pattern_count;
    }
    if (param_sum % redundancy_cmd->multiplier != 0) return 0;

    return 1;
}

int main() {
    char program[MAX_SIZE];
    size_t len = fread(program, 1, MAX_SIZE - 1, stdin);
    program[len] = '\0';

    return validate_program(program) ? 0 : 1;
}
