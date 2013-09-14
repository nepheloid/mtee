/* This is a simple tool to show the unsigned int definitions of the
 * Linux input event constants used by the entropy-source python script.
 * Use this only if you need to correct the constants in entropy-source.
 * Some of the Linux input event constants are not generated in a portable
 * way under Python. To work around this, you can compile the following
 * tiny C program which will print out the value of the command constants.
 * This should get around any issues with word size and endianess.
 *
 * Build with
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

