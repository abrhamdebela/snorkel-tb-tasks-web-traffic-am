#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <signal.h>
#include <unistd.h>
#include <pthread.h>

#define MAX_QUEUE 10000

typedef struct QueueNode {
    char *path;
    struct QueueNode *next;
} QueueNode;

typedef struct {
    QueueNode *head;
    QueueNode *tail;
    size_t count;
    pthread_mutex_t lock;
} Queue;

Queue g_queue;
char *g_root_path = NULL;
volatile int g_running = 1;

void sigint_handler(int sig) {
    printf("\n[INTERRUPT] Stopping backup...\n");
    g_running = 0;
    
    printf("Root path: %s\n", g_root_path);
    printf("Queue size: %zu\n", g_queue.count);
    
    pthread_mutex_lock(&g_queue.lock);
    QueueNode *node = g_queue.head;
    while (node) {
        QueueNode *next = node->next;
        free(node->path);
        free(node);
        node = next;
    }
    pthread_mutex_unlock(&g_queue.lock);
    
    free(g_root_path);
    exit(1);
}

void queue_init(Queue *q) {
    q->head = NULL;
    q->tail = NULL;
    q->count = 0;
    pthread_mutex_init(&q->lock, NULL);
}

void queue_push(Queue *q, const char *path) {
    QueueNode *node = malloc(sizeof(QueueNode));
    node->path = malloc(strlen(path) + 1);
    strcpy(node->path, path);
    node->next = NULL;
    
    pthread_mutex_lock(&q->lock);
    if (q->tail) {
        q->tail->next = node;
    } else {
        q->head = node;
    }
    q->tail = node;
    q->count++;
    pthread_mutex_unlock(&q->lock);
}

char *queue_pop(Queue *q) {
    pthread_mutex_lock(&q->lock);
    if (!q->head) {
        pthread_mutex_unlock(&q->lock);
        return NULL;
    }
    
    QueueNode *node = q->head;
    q->head = node->next;
    if (!q->head) {
        q->tail = NULL;
    }
    q->count--;
    pthread_mutex_unlock(&q->lock);
    
    char *path = node->path;
    free(node);
    return path;
}

void scan_directory(const char *path) {
    DIR *dir = opendir(path);
    if (!dir) return;

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL && g_running) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }

        char full_path[1024];
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);

        struct stat st;
        if (stat(full_path, &st) == 0) {
            if (S_ISDIR(st.st_mode)) {
                queue_push(&g_queue, full_path);
            } else {
                printf("FILE: %s\n", full_path);
            }
        }
        usleep(8000);
    }
    closedir(dir);
}

void *worker_thread(void *arg) {
    while (g_running) {
        char *path = queue_pop(&g_queue);
        if (path) {
            printf("Processing: %s\n", path);
            scan_directory(path);
            free(path);
        } else {
            usleep(50000);
        }
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory>\n", argv[0]);
        return 1;
    }

    signal(SIGINT, sigint_handler);
    
    queue_init(&g_queue);
    
    g_root_path = malloc(strlen(argv[1]) + 1);
    strcpy(g_root_path, argv[1]);
    
    printf("Multi-threaded backup starting: %s\n", g_root_path);
    
    pthread_t workers[4];
    for (int i = 0; i < 4; i++) {
        pthread_create(&workers[i], NULL, worker_thread, NULL);
    }
    
    scan_directory(g_root_path);
    
    while (g_queue.count > 0 && g_running) {
        usleep(100000);
    }
    
    g_running = 0;
    
    for (int i = 0; i < 4; i++) {
        pthread_join(workers[i], NULL);
    }
    
    free(g_root_path);
    pthread_mutex_destroy(&g_queue.lock);
    
    printf("\nBackup complete!\n");
    return 0;
}
