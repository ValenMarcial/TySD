# udp_server.py
import socket
import struct

HOST = "0.0.0.0"
PORT = 8000
BUFFER_SIZE = 2048  # Suficiente para cabecera (2B) + payload (1024B)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"[*] Servidor UDP listo y escuchando en {HOST}:{PORT}")

while True:
    print("\n[*] Esperando nueva transferencia...")
    file_handle = None
    expected_seq = 0
    client_address = None

    while True:
        packet, addr = server_socket.recvfrom(BUFFER_SIZE)
        if len(packet) < 2:
            continue

        pkt_type, seq_num = struct.unpack("!BB", packet[:2])
        payload = packet[2:]

        # Enviar siempre el ACK del paquete recibido
        ack_packet = struct.pack("!BB", 3, seq_num)
        server_socket.sendto(ack_packet, addr)

        # Si coincide con el número de secuencia esperado, procesamos
        if seq_num == expected_seq:
            if pkt_type == 0:
                # Inicio: payload contiene el nombre del archivo
                filename = "recv_" + payload.decode("utf-8", errors="ignore")
                file_handle = open(filename, "wb")
                print(f"[+] Iniciando recepción de: {filename} desde {addr}")
                expected_seq = 1 - expected_seq

            elif pkt_type == 1:
                # Datos del archivo
                if file_handle:
                    file_handle.write(payload)
                expected_seq = 1 - expected_seq

            elif pkt_type == 2:
                # Fin de archivo (EOF)
                print(f"[✓] Archivo transferido exitosamente.")
                if file_handle:
                    file_handle.close()
                break
        else:
            # Paquete duplicado: ya enviamos el ACK arriba, no escribimos en disco
            pass