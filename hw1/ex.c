#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char msg[1024] = "GET /member/palladio.JPG HTTP/1.0\r\n";
    printf(msg);
    printf("%d", (int)strlen(msg));
    strcat(msg, "Host: netapp.cs.kookmin.ac.kr\r\n");
    printf(msg);
    printf("%d", (int)strlen(msg));

    return 0;
}