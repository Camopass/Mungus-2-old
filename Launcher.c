#include <stdio.h>
#include <Windows.h>
#include <stdlib.h>

int main() {
    FreeConsole();

    char buff[MAX_PATH];
    GetCurrentDirectory(MAX_PATH, buff);
    char buff2[MAX_PATH];

    size_t dest_size = sizeof(buff);
    strncpy(buff2, buff, dest_size);
    buff2[dest_size - 1] = '\0';

    printf("%s", buff);

    strcat(buff, getenv("PATH"));
    strcat(buff2, "/main.py");
    strcat(buff, buff2);

    printf("%s", buff);

    WinExec(buff, SW_HIDE);
    return 0;
}