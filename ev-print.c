/* Build with
 *     make ev-print
 * or
 *     gcc ev-print.c -o ev-print
 * */
#include <stdio.h>
#include <linux/input.h>
int main (int argc, char *argv[]) {
    printf("EVIOCGNAME(255): %u\n", EVIOCGNAME(255));
    printf("EVIOCGBIT(0, 255): %u\n", EVIOCGBIT(0, 255));
    printf("EVIOCGID: %u\n", EVIOCGID);
    printf("EVIOCGVERSION: %u\n", EVIOCGVERSION);
}

