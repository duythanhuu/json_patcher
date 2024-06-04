#include <stdio.h>

int main() {
    FILE *file;
    char ch;

    file = fopen("file.txt", "r"); // replace "file.txt" with your file path
    if (file == NULL) {
        printf("Cannot open file \n");
        return 0;
    }

    ch = fgetc(file);
    while (ch != EOF) {
        putchar(ch);
        ch = fgetc(file);
    }

    int a= 0x10;
    int b= 0x20;

    fclose(file);
    return 0;
}