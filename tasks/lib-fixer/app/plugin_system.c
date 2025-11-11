/**
 * Plugin System: Application that loads plugins dynamically
 */

#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>

typedef void (*plugin_init_func)(void);
typedef void (*plugin_run_func)(void);

int load_plugin(const char* plugin_path) {
    printf("Loading plugin: %s\n", plugin_path);
    
    void* handle = dlopen(plugin_path, RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "Error loading plugin: %s\n", dlerror());
        return 1;
    }
    
    dlerror();
    
    plugin_init_func init = (plugin_init_func)dlsym(handle, "plugin_init");
    const char* error = dlerror();
    if (error) {
        fprintf(stderr, "Error finding plugin_init: %s\n", error);
        dlclose(handle);
        return 1;
    }
    
    plugin_run_func run = (plugin_run_func)dlsym(handle, "plugin_run");
    error = dlerror();
    if (error) {
        fprintf(stderr, "Error finding plugin_run: %s\n", error);
        dlclose(handle);
        return 1;
    }
    
    init();
    run();
    
    dlclose(handle);
    return 0;
}

int main(int argc, char* argv[]) {
    printf("=== Plugin System ===\n\n");
    
    if (argc < 2) {
        printf("Usage: %s <plugin.so> [plugin2.so ...]\n", argv[0]);
        return 1;
    }
    
    for (int i = 1; i < argc; i++) {
        if (load_plugin(argv[i]) != 0) {
            printf("Failed to load plugin: %s\n", argv[i]);
        }
        printf("\n");
    }
    
    printf("=== Plugin system test complete ===\n");
    return 0;
}

