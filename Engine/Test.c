#include <stdio.h>
#include <math.h>
#include <Python.h>

double get_c(int offset, int ticks) {
    double a = sin(ticks * 0.001 + offset);
    double b = a / 2 + 0.5;
    return b;
}

int main() {
    printf("Hello, World!\n");
    printf("%f \n", get_c(0, 100));
    print_bel();
    return 0;
}
