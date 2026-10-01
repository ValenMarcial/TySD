import socket
import os
import signal

HOST = ""
PORT = 65432

def handle_connection(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.send(data.upper())

def main():
    # Cada vez que un proceso hijo cambia de estado (termina o muere)
    # configuramos que se ignore la señal de salida del hijo con SIG_IGN
    # asi eñ kernel destruye el proceso hijo
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    with socket.socket(socket.AT_INET, socket.SOCK_STREAM) as s:
        # Permite recibir conexiones aunque el socket este en TIME_WAIT
        # Si otro proceso intenta hacer bind() no va a poder pero si esta en TIME_WAIT si por que significa que termino
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            pid = os.fork()
            if pid == 0:
                # El hijo no necesita el socket solo necesita la conexion
                s.close()
                handle_connection(conn, addr)
            else:
                # El proceso hijo termino por lo tanto podemos cerrar la conexion
                conn.close()
    

if __name__ == "__main__":
    main()