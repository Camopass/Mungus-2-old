#include <stdio.h>
#include <Windows.h>

int main() {
    FreeConsole();

    char buff[MAX_PATH];
    GetCurrentDirectory(MAX_PATH, buff);
    char buff2[MAX_PATH];

    size_t dest_size = sizeof(buff);
    strncpy(buff2, buff, dest_size);
    buff2[dest_size - 1] = '\0';

    strcat(buff, "/venv/Scripts/pythonw.exe ");
    strcat(buff2, "/main.py");
    strcat(buff, buff2);

    WinExec(buff, SW_HIDE);
    return 0;
}