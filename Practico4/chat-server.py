# Tcp Chat server
import socket, select

# List to keep track of socket descriptors
connections = []
port = 3000

# send message to other clients
def broadcast(sock, message):
    for socket in connections:
        if socket != server_socket and socket != sock:
            try:
                socket.send(bytes(message + '\n', "utf-8"))
            except:
                print(f"Something wrong with {socket}\n{error}")
                socket.close()
                connections.remove(socket)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", port))
server_socket.listen(10)

# Add server socket to the list of readable connections
connections.append(server_socket)
print(f"Chat server started on {server_socket} ")

while True:
    # Get the list sockets which are ready to be read through select
    read,write,error = select.select(connections,[],[])

    for sock in read:
        if sock == server_socket:
            #New connection
            sockfd, addr = server_socket.accept()
            connections.append(sockfd)
            print(f"Client {addr} connected")
            broadcast(sockfd, f"Client {addr} joined to chat")
        else:
            # Data received from some client, process it
            try:
                data = sock.recv(1024)
                if data:
                    data = data.decode('utf-8').strip()
                    print(f'data: [{data}]')
                    msg = str(sock.getpeername()) + ': ' + data
                    broadcast(sock, msg)
                    if str(data) == 'quit':
                        connections.remove(sock)
            except:
                print(f"Client {addr} disconnected")
                broadcast(sock, f"Client {addr} is offline")
                sock.close()
                connections.remove(sock)

server_socket.close()
