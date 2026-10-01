from socket import*
import sys
import select

HOST = 'localhost'
PORT = 3000
s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

exit = False

while not exit:
    socket_list = [sys.stdin, s]

    # Get the list sockets which are readable
    read, write, error = select.select(socket_list, [], [])

    for sock in read:
        if sock == s:
            #incoming message from remote server
            data = sock.recv(1024)
            if data:
                print("New message: " + data.decode('utf-8').strip())
        else:
            #user entered data by stdin
            msg = sys.stdin.readline()
            s.send(bytes(msg, "utf-8"))
            if msg.strip() == "quit":
                exit = True;

s.close()
