#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>

typedef struct {
    char *path;
    size_t size;
    time_t mtime;
} FileInfo;

FileInfo *g_file_list = NULL;
size_t g_file_count = 0;
size_t g_file_capacity = 0;
char *g_backup_root = NULL;

void sigint_handler(int sig) {
    fprintf(stderr, "\n\n=== BACKUP INTERRUPTED ===\n");
    fprintf(stderr, "Files scanned: %zu\n", g_file_count);
    
    if (g_backup_root != NULL) {
        fprintf(stderr, "Backup root: %s\n", g_backup_root);
    }
    
    fprintf(stderr, "Cleaning up...\n");
    
    for (size_t i = 0; i < g_file_count; i++) {
        free(g_file_list[i].path);
    }
    free(g_file_list);
    free(g_backup_root);
    
    fprintf(stderr, "Cleanup complete.\n");
    exit(130);
}

void add_file(const char *path, size_t size, time_t mtime) {
    if (g_file_count >= g_file_capacity) {
        g_file_capacity = (g_file_capacity == 0) ? 1024 : g_file_capacity * 2;
        g_file_list = realloc(g_file_list, g_file_capacity * sizeof(FileInfo));
    }
    
    g_file_list[g_file_count].path = malloc(strlen(path) + 1);
    strcpy(g_file_list[g_file_count].path, path);
    g_file_list[g_file_count].size = size;
    g_file_list[g_file_count].mtime = mtime;
    g_file_count++;
}

void scan_directory(const char *path, int depth) {
    if (depth > 20) {
        return;
    }

    DIR *dir = opendir(path);
    if (!dir) {
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }

        char full_path[2048];
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);

        struct stat st;
        if (stat(full_path, &st) == 0) {
            if (S_ISDIR(st.st_mode)) {
                printf("[D] %*s%s/\n", depth * 2, "", entry->d_name);
                scan_directory(full_path, depth + 1);
            } else if (S_ISREG(st.st_mode)) {
                printf("[F] %*s%s (%ld bytes)\n", depth * 2, "", entry->d_name, st.st_size);
                add_file(full_path, st.st_size, st.st_mtime);
            }
        }

        usleep(5000);
    }

    closedir(dir);
}

void print_summary() {
    printf("\n=== BACKUP SUMMARY ===\n");
    printf("Total files: %zu\n", g_file_count);
    
    size_t total_size = 0;
    for (size_t i = 0; i < g_file_count; i++) {
        total_size += g_file_list[i].size;
    }
    
    printf("Total size: %.2f MB\n", total_size / (1024.0 * 1024.0));
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory_to_backup>\n", argv[0]);
        return 1;
    }

    struct sigaction sa;
    sa.sa_handler = sigint_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);

    g_backup_root = malloc(strlen(argv[1]) + 1);
    strcpy(g_backup_root, argv[1]);

    printf("Backup Tool v1.0\n");
    printf("================\n");
    printf("Scanning: %s\n", g_backup_root);
    printf("Press Ctrl-C to interrupt...\n\n");

    scan_directory(g_backup_root, 0);
    
    print_summary();

    for (size_t i = 0; i < g_file_count; i++) {
        free(g_file_list[i].path);
    }
    free(g_file_list);
    free(g_backup_root);
    g_backup_root = NULL;

    return 0;
}
