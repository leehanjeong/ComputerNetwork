import socket
import sys
import os

BUF_SIZE = 1024

def send_response_msg(msg, client_socket):

    file_name = msg.split('\r\n')[0].split('/')[1].split()[0]
    send_size = 0
    file_size = 0
    extension = file_name.split('.')[1]
    #print('extension', extension)

    # 해당하는 파일을 찾아서 HTTP Response 메세지로 만들어서 브라우저로 보낸다.
    if extension == 'html':
        try:
            file_size = os.path.getsize(file_name)
        except:
            response_msg = 'HTTP/1.0 404 NOT FOUND\r\nConnection: close\r\nContent-Length: 0\r\nContent-Type: text/html\r\n\r\n'.encode()
            client_socket.send(response_msg)
        else:
            response_msg = ('HTTP/1.0 200 OK\r\nConnection: close\r\nContent-Length: {}\r\nContent-Type: text/html\r\n\r\n'.format(file_size)).encode()
            client_socket.send(response_msg)

            with open(file_name, 'rb') as f:
                data = f.read(BUF_SIZE)
                while data:
                    send_size += client_socket.send(data)
                    data = f.read(BUF_SIZE)

    elif extension == 'jpg':
        try:
            file_size = os.path.getsize(file_name)
        except:
            response_msg = 'HTTP/1.0 404 NOT FOUND\r\nConnection: close\r\nContent-Length: 0\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
            client_socket.send(response_msg)
        else:
            response_msg = ('HTTP/1.0 200 OK\r\nConnection: close\r\nContent-Length: {}\r\nContent-Type: image/jpeg\r\n\r\n'.format(file_size)).encode()
            client_socket.send(response_msg)

            with open(file_name, 'rb') as f:
                data = f.read(BUF_SIZE)
                while data:
                    send_size += client_socket.send(data)
                    data = f.read(BUF_SIZE)

    return send_size, file_size, file_name


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Write port number.")
        exit()

    print("Student ID: 20191650")
    sys.stdout.flush()
    print("Name: Hanjeong Lee")
    sys.stdout.flush()

    port_num = int(sys.argv[1])
    ip = '127.0.0.1'

    # 브라우저에 http://localhost:10000/palladio.jpg를 입력하고 엔터를 치면 palladio.jpg 파일을 서버로 요청. 이 HTTP Request 메시지의 첫번째 라인과 User-Agent 정보를 출력. 헤더 필드의 수도 출력.
    # 그리고 해당하는 파일을 찾아서 HTTP Response 메시지로 만들어서 브라우저로 보냄
    # 다 보내고 나면 실제 전송한 바이트 수와 파일의 바이트 수를 출력. 이 둘은 같아야 정상.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((ip, port_num))
    server_socket.listen()

    while True:
        client_socket, client_addr = server_socket.accept()
        request_msg = client_socket.recv(BUF_SIZE).decode()
        # print(request_msg)

        header = request_msg.split('\r\n\r\n')[0]
        header_field_num = len(header.split('\r\n'))-1

        print('Connection : Host IP {}, Port {}, socket {}'.format(client_addr[0], client_addr[1], client_socket.fileno()))
        sys.stdout.flush()
        print(request_msg)
        sys.stdout.flush()
        print('{} headers'.format(header_field_num))
        sys.stdout.flush()

        send_size, file_size, filename = send_response_msg(request_msg, client_socket)
        if send_size > 0 and file_size > 0:
            print('finish {} {}\n'.format(send_size, file_size))
            sys.stdout.flush()
        else:
            print('Server Error : No such file ./{}!\n'.format(filename))
            sys.stdout.flush()
        client_socket.close()

    server_socket.close()