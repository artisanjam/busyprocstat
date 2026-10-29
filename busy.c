#include <stdio.h>

#define NEVER -1
#define TRUE 1
#define ARRAY_SIZE 1024
#define MESSAGE "Burning CPU Cycles..."

int main(void) {
    volatile int array[ARRAY_SIZE];

    puts(MESSAGE);
    // Initialize array to do some busy work
    for(int i = 0; i < ARRAY_SIZE; i++) {
        array[i] = 0;
    }
    while(TRUE) {
        // Loop forever doing busy work
        for(int i = 0; i < ARRAY_SIZE; i++) {
            array[i]++;
        }
    }
    return NEVER;
}
