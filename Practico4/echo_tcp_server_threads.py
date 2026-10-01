import socket
import threading

HOST = ""
PORT = 65432

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Permite recibir conexiones aunque el socket este en TIME _WAIT
        # Si otro proceso intenta hacer bind() no va a poder pero si esta en TIME_WAIT si por que significa que termino
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen()
        
        while True:
            conn, addr = s.accept()
            client = threading.Thread(target=handle_connection, args=(conn, addr), daemon=True)
            client.start()

if __name__ == "__main__":
    main()