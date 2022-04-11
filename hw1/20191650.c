#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>

// 한 문장 뒤에는 \r\n 붙여야함


// TODO 2. 프로그램은 주어진 파라미터를 기반으로 HTTP Request 메시지를 생성한다. 이 과제에서는 HTTP request 메시지는 아래의 3개의 헤더라인만 포함하면 된다.
// GET /member/palladio.JPG HTTP/1.0
// Host: netapp.cs.kookmin.ac.kr
// User-agent: HW1/1.0
// Connection: close

// TODO 3. 프로그램이 HTTP response 메시지를 받으면 Content-Length 헤더 필드를 찾아서 그 파일의 크기를 찾아내야 한다. 그리고, 그 파일의 크기를 아래와 같이 표시한다. 
// Total Size 142740 bytes

// TODO 4. 또한, 파일을 다운로드할 때 다운로드 상태를 출력한다. 매 10%를 넘어갈 때마다 아래와 같은 메시지를 출력한다. 단, 파일이 작아서 한번에 10% 이상 (예를 들어 20~100%) 도착할 경우, 그 상태를 출력하면 된다.
// Current Downloading 16382/142740 (bytes) 11%
// Current Downloading 65464/142740 (bytes) 44%

// TODO 5. 다운로드를 다 마치면, 아래와 같은 메시지를 출력한다.
// Download Complete: palladio.JPG, 142740/142740

int main(int argc, char *argv[]) {
    struct hostent *hostp;
    struct sockaddr_in server;
    int sock, bytesread;

    char buf[BUFSIZ]; // BUFSIZE 바꾸기
    
    // make request msg
    char msg[BUFSIZ] = "GET /member/palladio.JPG HTTP/1.0\r\n";
    strcat(msg, "Host: netapp.cs.kookmin.ac.kr\r\n");
    strcat(msg, "User-agent: HW1/1.0\r\n");
    strcat(msg, "Connection: close\r\n\r\n");

    // make receive msg
    char recv_msg[BUFSIZ];


    // print info
    printf("Student ID : 20191650\nName : Hanjeong Lee\n");

    // arg error
    int (argc != 3) {
        fprintf(stderr, "usage: %s host port\n", argv[0]);
    }

    // make socket
    if((sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        perror("socket");
        exit(1);
    }

    // get host
    if((hostp = gethostbyname(argv[1])) == 0) { 
        fprintf(stderr, "%s: unknown host\n", argv[1]); 
        exit(1);
    }

    // set server
    memset((void *) &server, 0, sizeof(server));
    server.sin_family = AF_INET;
    memcpy((void *) &server.sin_addr, hostp->h_addr, hostp->h_length);
    server.sin_port = htons((u_short)atoi(argv[2])); // 포트 지정, little endian -> big endian

    // connect server
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) { // socket을 통해 server에 연결
        close(sock);
        fprintf(stderr, "connect\n");
        exit(1);
    }

    send(sock, msg, strlen(msg), 0); // send request
    bytesread = recv(sock, recv_msg, BUF_SIZE, 0); // receive

    recv_msg[bytesread] = '\0';
    printf("s\n", recv_msg);

    // 여기는 성환오빠 코드
    char *status = malloc(3);
    strncpy(status, response_msg + 9, 3);
    // printf("status: %s\n", status);
    int status_code = atoi(status);
    int start_response = strlen(response_msg);
    // printf("status_code: %d, start_response: %d\n", status_code, start_response);

    switch (status_code)
    {
    case 200:
        break;
    case 301:
        printf("%d Moved Permanently\n", status_code);
        PROMPT();
        continue;
        break;
    case 400:
        printf("%d Bad request\n", status_code);
        PROMPT();
        continue;
        break;
    case 404:
        printf("%d Not Found\n", status_code);
        PROMPT();
        continue;
        break;
    case 505:
        printf("%d HTTP Version Not Supported\n", status_code);
        PROMPT();
        continue;
        break;
    }
    free(status);

    // get content size
    char *filesize = strtok(response_msg, "\n");

    while (filesize != NULL)
    {
        filesize = strtok(NULL, ":"); // 앞에서 자른애 이어서 자르는거임 따라서 response_msg 분석 필요. null 될 때 까지이어서 자름.
        if (strcmp(filesize, "Content-Length") == 0)
        {
            filesize = strtok(NULL, "\n");
            break;
        }
        filesize = strtok(NULL, "\n");
    }
    int total_size = atoi(filesize);
    printf("Total Size %d bytes\n", total_size);

    char *body_data = strtok(NULL, "\n");
    // printf("receive_data: %s\n", receive_data);

    // seperate header
    while (body_data[0] != '\r')
    {
        body_data = strtok(NULL, "\n");
    }
    body_data = strtok(NULL, "\n");

    FILE *fp = fopen(fname, "wb");

    int start_body = strlen(body_data);

    // Don't write if HTTP response header has no data
    if (*body_data != 0)
    {
        // seperate header size
        fwrite(body_data, bytesread - (start_response - start_body), 1, fp);
    }
    int i = 1, download = 0;
    while (true)
    {
        // Receive data left in socket
        memset(response_msg, 0, sizeof response_msg);
        int recv_data_size = recv(sock, response_msg, sizeof response_msg, 0);
        response_msg[recv_data_size] = '\0';

        // Complete download if downloaded file size is same or bigger than content length
        if (download >= total_size)
        {
            printf("Download Complete: %s, %d/%d\n", fname, download, total_size);
            break;
        }

        // Write received data from socket
        fwrite(response_msg, recv_data_size, 1, fp);

        // Check current download size
        download = ftell(fp);

        if (download >= (total_size / 10) * i)
        {
            printf("Current Downloading %d/%d (bytes) %d%%\n", download, total_size, (int)(download * 100 / total_size));
            i++;
        }
    }

    close(sock);

    return 0;
}