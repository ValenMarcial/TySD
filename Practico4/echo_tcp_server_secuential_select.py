import socket
import select

HOST = ""
PORT = 65432

# 1. Crear el socket principal pasivo (de escucha)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
# Modo no bloqueante para evitar que llamadas a accept/recv congelen el loop
# Si queres hacerlo con bloqueo hay que configurarle timeout para que no bloquee indefinidamente el loop
# pero pensa que eso va a bloquear a todas las demas conexiones
server_socket.setblocking(False)

print(f"[*] Servidor TCP con select() escuchando en el puerto {PORT}...")

# Lista de descriptores a monitorear para lectura (sockets_list)
# Arrancamos monitoreando únicamente el socket de bienvenida/escucha
# por que cualquier conexion entrante se considera evento de lectura
inputs = [server_socket]

while True:
    # select() suspende el proceso hasta que algún socket esté listo para leer
    # primer parametro son los sockets a vigilar para saber si tienen datos para leer
    # segundo parametro es la lista de sockets que quiero vigilar si el buffer de saluda tiene espacio libre y podes mandar datos sin bloquear
    # tercer parametro es la lista de sockets a vigilar por errores 
    readable, _, exceptional = select.select(inputs, [], inputs)

    for s in readable:
        if s is server_socket:
            # CASO A: Hay actividad en el socket principal -> Llegó un nuevo cliente
            # Esta linea deberia estar en un try catch por que es un metodo bloqueante pero como esta desactivado el bloqueo el error hace que explote
            conn, addr = s.accept()

            conn.setblocking(False)
            inputs.append(conn)  # Agregamos el nuevo socket al conjunto de monitoreo
            print(f"[+] Conexión aceptada de {addr}")
        else:
            # CASO B: Hay actividad en un socket de cliente existente -> Llegaron datos o FIN
            # Esta linea deberia estar en un try catch por que es un metodo bloqueante pero como esta desactivado el bloqueo el error hace que explote
            data = s.recv(1024)
            if data:
                # Se recibieron datos: procesar y responder
                # Esta linea deberia estar en un try catch por que es un metodo bloqueante pero como esta desactivado el bloqueo el error hace que explote
                s.send(data.upper())
            else:
                # Llegó un EOF / FIN (data == b"") -> El cliente cerró la conexión
                print(f"[-] Cliente desconectado {s.getpeername()}")
                inputs.remove(s)  # Se deja de monitorear
                s.close()         # Se cierra el socket

    # Manejo de sockets con condiciones excepcionales/errores
    for s in exceptional:
        inputs.remove(s)
        s.close()