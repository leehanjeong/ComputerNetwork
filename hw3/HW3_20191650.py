import socket
import sys
import os
import select
import msvcrt

BUF_SIZE = 1024

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Write appropriate argument")
        exit()

    port_num = int(sys.argv[1])
    user_id = sys.argv[2]
    user_name = sys.argv[3]

    print("Student ID: 20191650")
    sys.stdout.flush()
    print("Name: Hanjeong Lee")
    sys.stdout.flush()

    connection_list = []

    # 서버 만듦
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1' # 바꿔도 되나?
    server_socket.bind((ip, port_num))
    server_socket.listen()

    #input_list = [server_socket, sys.stdin] # ubuntu ver.
    input_list = [server_socket,] # win ver.
    socket_list = [] #소켓으로 쿼리 메세지가 오면 다른 소켓들로 보냄.  소켓 생성될 때마다 추가. 포룹 돌면서 여기에 저장된 소켓을 이용하여 메세지 보냄
    while True:
        # select 공부~
        readable, writable, exceptinal = select.select(input_list, [], [], 10) # file descriptor to read / write/ error
        if msvcrt.kbhit(): # win ver.
            readable.append(sys.stdin)
        # select는 읽을 fd 없으면 block. 다시 생길 때까지 block 하는 것
        for readable_sock in readable:
            print(readable_sock)
            if readable_sock == sys.stdin: # 입력인 경우
                msg = sys.stdin.readline()
                msg_list = msg.split()
                if msg_list[0] == '@connect':
                    host_name = msg_list[1]
                    port = int(msg_list[2])
                    client_socket.connect((host_name, port))
                    input_list.append(client_socket)
                    
                elif msg_list[0] == '@query':
                    peer_id = msg_list[1]
                    port = int(peer_id+'000')
                    hop = 0
                    # for sock in readable:

                    # msg = 'Query '+ 'qs' + 'qseq' + 'hop' + peer_id
                    # #flooding
                elif msg_list[0] == '@quit':
                    exit()
                else:
                    msg = user_id + ':' + msg
                    client_socket.send(msg.encode())
                #msg 처리
            elif readable_sock == server_socket: # 서버인 경우 recv안 함??
                client_socket, client_addr = server_socket.accept()
                input_list.append(client_socket)
                print(f'new connection from host {client_addr[0]}, sd {client_socket.fileno()}')
            else: # client 소켓인 경우 readablel_sock.send(server_socket.recv(BUF_SIZE).decode().encode())
                # readable_sock.send(data.encode())
                data = readable_sock.recv(BUF_SIZE).decode()
                if data: # 클라이언트에 데이터가 들어온 경우
                    print(readable_sock.getpeername(), data)
                else: # 데이터가 없는 경우(클라이언트에서 소켓 close 한 경우)
                    print(f'Connection Closed {readable_sock.fileno()}')
                    readable_sock.close()
                    input_list.remove(readable_sock)

    server_socket.close()

    # 1. 연결 -> 호스트와 포트번호를 이용하여 TCP 연결을 설정한다. 연결 된 TCP 정보 잘 저장해야함
    # 2. query -> 특정 사용자 찾기. what is 질의번호?  hop은 fowarding 한 회수



    # ## Connect to an IP with Port, could be a URL
    # sock.connect(('0.0.0.0', 8080))
    # ## Send some data, this method can be called multiple times
    # sock.send("Twenty-five bytes to send")
    # ## Receive up to 4096 bytes from a peer
    # sock.recv(4096)
    # ## Close the socket connection, no more data transmission
    # sock.close()
    
    # 우선 서버 역할을 하는 소켓 하나를 만들고 연결 요청이 들어오면 자동으로 새로운 소켓을 만듦. 사용자가 연결을 요청하면 그 때 클라이언트 소켓을 만들어서 연결 요창을 함.
    # 만들어진 여러개의 소켓에서 메시지가 들어올 수 있고, 특히 키보드에서 입력이 들어올 수 있기 때문에 소켓과 키보드에서 입력이 들어오는지 동시에 감시해야함. 수업시간에 select 설명함

    # 1) “@connect” 명령
    # 파라미터로 주어진 호스트와 포트번호를 이용하여 TCP 연결을 설정한다. 각 사용자는 자신과 연결된 TCP 연결에 대한 정보를 잘 저장하고 있어야 한다.

    # 2) “@query”
    # 이 명령어는 질의 메시지를 생성한다. 그 메시지의 이름이나 포맷은 적절하게 결정하면 된다. 당연히 찾고자 하는 아이디 정보는 포함되어야 한다. 위 예제에서는 QUERY라는 이름을 가지는 메시지를 생성하였고, 그 포맷은 그냥 아래와 같은 1줄짜리 문자열이었다.
    # QUERY qs qseq hop pid
    # qs: 보낸 사람 아이디
    # qseq: 보낸 사람이 생성한 질의 번호
    # hop: forwarding 한 회수
    # pid: 찾고자 하는 사용자 아이디
    # 어쨌든 생성된 메시지는 해당 사용자와 연결된 다른 모든 사용자 프로그램으로 전달된다. 이러한 방식을 flooding이라고 한다.

    # 이 질의 메시지를 받은 사용자 프로그램은 이 메시지를 분석하여, 우선 이 메시지가 전에도 들어왔는지를 검사하고, 이전에 들어온 메시지라면 무시한다.
    # 처음 받은 질의 메시지라면 아래와 같이 처리한다.
    # 1) 자신의 아이디와 같은 아이디를 찾는 경우: 바로 응답 메시지를 생성해서 보낸다. 위 예에서는 QUERYHIT라는 응답 메시지를 생성해서 보냈다.
    # 2) 주어진 질의 메시지의 내용이 자신을 찾는 것이 아닌 경우: 메시지가 들어온 연결을 제외한 다른 모든 연결로 메시지를 복사해서 전달한다. 메시지를 전달할 때마다 몇 번의 사용자를 거쳤는지에 대한 정보를 저장하게 하여 이를 메시지에 포함시켜야 한다. 
    #    간단하게 QUERY 메시지 내에 counter 정보를 하나 추가해서 다른 사용자에게 forwarding 될 때마다 counter를 1씩 증가시키면 된다.
    # 3) 최종적으로 질의 메시지가 찾고자 하는 사용자에게 도착하면 이 사용자는 응답 메시지를 생성해서 최초 질의한 사용자에게 전송한다. 이 때 이 응답 메시지는 해당질의 메시지가 도달한 경로를 통해서 최초 질의자에게 도착하도록 해야 한다. 
    #    절대로 flooding 방식을 사용하면 안 된다.
    # 4) 메시지를 받을 때에는 어느 연결을 통해 받았는지를 저장하고 있어서 응답 메시지를 정상적으로 최초 질의자에게 전달할 수 있다.

    # 최초 질의자가 응답 메시지를 받으면 아래와 같은 형식으로 그 정보를 출력한다.
    # PeerInfo src <질의한 아이디> target <사용자 아이디> name <사용자 이름> IP <IP 주소> port <포트 번호> hop <hop 수>
    # 위 메시지를 이용하여 프로그램의 정확성을 검증하기 때문에 위 포맷대로 출력하면 된다.
    # 따라서 응답 메시지는 위 정보를 출력할 수 있는 내용을 포함하고 있어야 한다. 중간에 디버깅을 위해서 출력하는 메시지는 원하는대로 출력해서 사용하면 된다.
    # 아래의 예에서는 30번 아이디를 가진 사용자의 이름이 lee이라는 것을 알 수 있다. 그리고 IP 주소와 포트번호도 알 수 있다. 마지막 숫자 2는 대상 사용자가 질의한 사용자 10으로부터 2 hop 떨어져 있다는 것을 알 수 있다.
    # PeerInfo src 10 target 30 name lee IP 172.30.1.27 port 30000 hop 2