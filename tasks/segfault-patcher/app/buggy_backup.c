#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <signal.h>
#include <unistd.h>

char *g_backup_path = NULL;

void sigint_handler(int sig) {
    printf("\nBackup interrupted by user!\n");
    if (g_backup_path != NULL) {
        printf("Backup path was: %s\n", g_backup_path);
    }
    free(g_backup_path);
    exit(1);
}

void scan_directory(const char *path, int depth) {
    DIR *dir = opendir(path);
    if (!dir) {
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }

        char full_path[1024];
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);

        struct stat st;
        if (stat(full_path, &st) == 0) {
            if (S_ISDIR(st.st_mode)) {
                printf("DIR [%d]: %s\n", depth, full_path);
                scan_directory(full_path, depth + 1);
            } else {
                printf("FILE[%d]: %s (%ld bytes)\n", depth, full_path, st.st_size);
            }
        }

        usleep(10000);
    }

    closedir(dir);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory_to_backup>\n", argv[0]);
        return 1;
    }

    signal(SIGINT, sigint_handler);

    g_backup_path = malloc(strlen(argv[1]) + 1);
    strcpy(g_backup_path, argv[1]);

    printf("Starting backup of: %s\n", g_backup_path);
    printf("Press Ctrl-C to interrupt...\n\n");

    scan_directory(g_backup_path, 0);

    printf("\nBackup scan complete!\n");
    
    free(g_backup_path);
    g_backup_path = NULL;

    return 0;
}
