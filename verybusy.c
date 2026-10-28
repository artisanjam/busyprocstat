#include <stdio.h>
#include <pthread.h>

#define NEVER -1
#define TRUE 1
#define ARRAY_SIZE 1024
#define NUM_THREADS 32
#define MESSAGE "REALLY burning CPU cycles..."

void *busy(void *data) {
    volatile int array[ARRAY_SIZE];
    for(int i = 0; i < ARRAY_SIZE; i++) {
        array[i] = 0;
    }
    while(TRUE) {
        for(int i = 0; i < ARRAY_SIZE; i++) {
            array[i]++;
        }
    }
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS]; 
    puts(MESSAGE);
    for(int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, busy, NULL);
    }
    for(int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    return NEVER;
}
