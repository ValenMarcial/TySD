# udp_client.py
import os
import socket
import struct
import sys

TIMEOUT = 1.0       # Tiempo límite de espera de ACK (en segundos)
CHUNK_SIZE = 1024   # Tamaño de cada bloque de lectura
MAX_RETRIES = 10    # Máximo número de reintentos por paquete

def send_reliable(sock, server_addr, pkt_type, seq_num, payload=b""):
    header = struct.pack("!BB", pkt_type, seq_num)
    packet = header + payload

    for attempt in range(MAX_RETRIES):
        sock.sendto(packet, server_addr)
        try:
            ack_raw, _ = sock.recvfrom(16)
            if len(ack_raw) >= 2:
                ack_type, ack_num = struct.unpack("!BB", ack_raw[:2])
                # Verificamos si es un paquete de ACK y si el número coincide
                if ack_type == 3 and ack_num == seq_num:
                    return True
        except socket.timeout:
            pass  # Expiró el temporizador: vuelve a iterar y retransmite

    raise TimeoutError(f"No se recibió ACK para seq={seq_num} tras {MAX_RETRIES} intentos.")

def main():
    if len(sys.argv) != 4:
        print(f"Uso: python {sys.argv[0]} <archivo> <ip/host_servidor> <puerto>")
        sys.exit(1)

    filepath = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])
    server_addr = (server_ip, server_port)

    if not os.path.exists(filepath):
        print(f"[!] El archivo '{filepath}' no existe.")
        sys.exit(1)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    current_seq = 0
    filename = os.path.basename(filepath)

    print(f"[*] Conectando a {server_ip}:{server_port} para transferir: {filename}")

    # 1. Enviar Metadata (Tipo 0: Nombre del archivo)
    send_reliable(client_socket, server_addr, 0, current_seq, filename.encode("utf-8"))
    current_seq = 1 - current_seq

    # 2. Enviar Fragmentos de Datos (Tipo 1)
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            send_reliable(client_socket, server_addr, 1, current_seq, chunk)
            current_seq = 1 - current_seq

    # 3. Enviar Fin de Archivo / EOF (Tipo 2)
    # Se reintenta el EOF para asegurar que el servidor reciba la señal de cierre
    for _ in range(3):
        try:
            send_reliable(client_socket, server_addr, 2, current_seq, b"EOF")
            break
        except TimeoutError:
            pass

    print("[✓] Envío completado.")
    client_socket.close()

if __name__ == "__main__":
    main()