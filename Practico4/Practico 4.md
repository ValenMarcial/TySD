
# 1)
Para comunicar dos terminlec via TCP con netcat, una terminal es el servidor que escucha un puerto y la otra es el cliente que se conecta en ese puerto:

## Terminal 1 Servidor:
Usamos cualquier puerto mayor a 1024 ya que los menores o iguales a 1024 tienen privilegio de root.
```bash
nc -l -p 12345
```
- La flag `-l` hace que netcat se ponga en modo listen osea en escucha
- Al no especificar la direccion de escucha automaticamente se coloca la 0.0.0.0 en IPv4
osea escucha en todas las interfaces de red disponibles al mismo tiempo
- Si quisiera restringir a escuchar solo lo que llega a localhost deberia hacer `nc -l -s 127.0.0.1 -p 12345`
## Terminal 2 Cliente:
```bash
nc 127.0.0.1 12345
```
conectamos por nuestra red local propia en el host al puerto donde el servidor esta escuchando

## Aclaracion:
No hay que especificar que use TCP por que por defecto ya lo usa habria que especificar si queremos usar udp con la flag `-u`.
## Mandar mensajes:
Terminal 1:
`nc -l -s 127.0.0.1 -p 12345`
Terminal 2:
`echo "Hola, soy el cliente que envia mensaje por TCP al servidor" | nc -N 1237.0.0.1 12345`
La flag `-N` hace shutdown luego de enviar el mensaje osea hace EOF. Envia un paquete de FIN.

## Mandar archivos:
Terminal 1:
`nc -l -s 127.0.0.1 -p 12345 > archivo_destino.txt`
Terminal 2:
`nc -N 127.0.0.1 12345 < archivo_origen.txt`
Lo que sucede aca es que el contenido de archivo_origen.txt se redirige a la entrada standard (stdin) de nc  y se transmiten esos bytes a traves de TCP. Luego se redirige la salida estandar (stdout) de nc en el servidor para escribir los bytes que se reciban del cliente en archivo_destino.txt y luego cuando lee el paquete FIN cierra la conexion.

# 2)
### a) 
Para capturar los mensajes con tcpdump:
#### 1)
Levantar el proyecto kathara 
```bash
kathara check
kathara lstart
```
Configurar las redes dentro de cada pc
**en la pc1:**
```bash
ip addr add 192.168.1.10/24 dev eth0
```
**en la pc2:**
```bash
ip addr add 192.168.1.20/24 dev eth0
```

No hace falta configurar ninguna regla de ruteo, que directamente salgan por la default.

#### 2)
##### Ejercicio a y b
###### a) Crear el servidor de escucha
ejecutar el comando en una terminal de la pc1:
```bash
nc -u -l -s 192.168.1.10 -p 12345
```
con esto hacemos que se vea todo lo que llega a la red `192.168.1.10:12345` en la consola
la flag `-u` hace que se cree una conexion `UDP`

###### b) Leer los paquetes con tcpdump
en una terminal aparte ejecutar
```bash
kathara connect pc1
```
esto nos crea una nueva conexion con la pc1 y nos abre una terminal, en esta terminal ejecutamos 
```bash
tcpdump -i eth0 -A -s 0 'udp port 12345'
```
lo que hace esto es leer todo los paquetes que llegan por la interfaz eth0 por el puerto 12345
Para que se guarde en un archivo este contenido debemos ejecutar de esta forma
```bash
tcpdump -i eth0 -A -s 0 -w ./path/captura.pcap 'udp port 12345'
```
Para leer los paquetes 
###### c) Envio de paquetes desde pc2
en una terminal de la pc2 podemos mandar de diferentes formas los paquetes
1) Envio de un paquete solo
```bash
echo "Algun tipo de mensaje" | nc -u 192.168.1.10 12345
```
o de la siguiente forma con un puerto fijo desde el emisor
```bash
echo "Algun tipo de mensaje" | nc -u -p 56789 192.168.1.10 12345
```
de esta forma se envia el paquete y se mantiene la conexion y se ve en el servidor el contenido del primer paquete pero luego se mandan los demas paquete pero en el servidor no se ve mas nada por las stdout y la conexion queda persistente, esto pasa por algun problema del buffer de netcat, para dejar la conexion persistente lo que hay que hacer es crear un buffer y mandar por ahi.
2) Conexion persistente con envio interactivo
```bash
stdbuf -i eth0 nc -u 192.168.1.10 12345
```
asi vamos a crear un buffer donde podamos ir mandando los paquetes al servidor sin tener que mandar de a uno y se van a ver en la primer conexion del servidor por la stdout

###### Datos obtenidos del ejercicio
Gracias a ver que es lo que pasa en wireshark, cuando creamos una conexion UDP al puerto 12345 si se cae o se corta la conexion del emisor (cliente) el receptor (servidor) mantiene la conexion creada, por lo tanto si alguien intenta enviar un paquete a ese puerto queda bloqueado y UDP lo rechaza enviando un paquete de control avisando que el paquete fue rechazado con Port unrecheable.
En el caso de estar viva la conexion lo que sucede es que se envian los paquetes UDP y cada cierto tiempo se mandan los paquetes Who has de ARP.
El flag `-s` 0 le dice a tcpdump que capture toda la longitud del paquete

##### c)
En la consola de pc1 ejecutar
 ```bash
 nc -u -l -s 192.168.1.10 -p 12345
 ```
En otra consola de pc1 ejecutar
```bash
tcpdump -i eth0 -A -s 0 -nn -vv 'udp port 12345'
```
Lo que hace el flag -nn es no traducir el dominio y el puerto osea no va a buscar el DNS ni el significado del puerto.
Lo que hace el flag -vv es verificar el checksum y mostrarlo por pantalla

En la pc2 ejecutar
```bash
scapy -H
```
al enviar un paquete valido de esta forma:
```scapy
valid = IP(src="192.168.1.20", dst="192.168.1.10")/UDP(sport=6666, dport=12345)/"Hello"
send(valid)
```

![[Pasted image 20260930194456.png]]
Este paquete se ve en el servidor que esta escuchando

al enviar un paquete invalido de esta forma:
```scapy
invalid = IP(src="192.168.1.20", dst="192.168.1.10")/UDP(sport=6666, dport=12345,chksum=0x1234)/"Hello"
send(invalid)
```
![[Pasted image 20260930194728.png]]
Este paquete no se ve en el servidor que esta esuchando

tcpdump directamente interactua con la placa de red antes que el paquete llegue al kernel por eso lo ve.

no usamos sr1() por que asi envia y el cliente se queda esperando una respuesta bloqueando todo ya que usamos una conexion UDP si fuese TCP seria diferente en el caso de un paquete valido se envia y el servidor responde, y en el caso de un paquete con cheksum invalido el servidor no responde por que directamente se descarta apenas se ve, en cambio si fuese por puerto no disponible si se envia un paquete ICMP avisando Port Unrecheable. 


# 3)
Primero en la consola de la pc1 ponemos a escuchar el servidor TCP
```bash
nc -l -s 198.168.1.10 -p 12345
```
En otra consola podemos escuchar con tcpdump
como en los ejercicios anteriores, este lo realice con wireshark para ver los paquetes.
Ahora al momento de realizar la conexion del cliente que seria la pc2 sucede esto, ejecutamos:
```bash
nc 192.168.1.10 12345
```
al momento de ejecutar ese comando en la pc2 se produce el envio de estos paquetes
![[Pasted image 20260930202404.png]]
estos paquetes son el handshake entre el cliente y el servidor.
- El cliente envia un paquete SYN para sincronizar con el servidor, ese paquete 1 lleva un seq que es un numero de 32bits y representa el numero de secuencia, en wireshark lo vemos como 0 pero en realidad es un numero grande, si es el primer paquete el seq se genera. El primer paquete no tiene valor en ACK ya que la bandera ACK no esta activa.
- El segundo paquete es el servidor que responde al cliente con un paquete SYN + ACK donde se envia el valor de seq que  lo que hace es generar el primer seq y manda ese y el valor de ACK que seria el seq del cliente mas 1.
- El cliente recibe estos paquetes y le envia el servidor un ACK con el valor del seq del servidor mas 1.
Con esta secuencia se realiza el apreton de manos entre el cliente y el servidor para comenzar a enviar paquetes de forma full duplex.

Una vez el cliente se desconecta se produce esto
![[Pasted image 20260930215811.png]]
- El cliente envia un paquete FIN + ACK que lo que hace es avisar al servidor que ese fue su ultimo paquete y que el anterior que habia mandado el servidor lo recibio de manera correcta.
- El servidor le contesta con un paquete FIN + ACK que le avisa al cliente que ese fue su ultimo paquete y el ACK que nos dice que recibio correctamente el paquete de FIN.
- El cliente contesta al servidor con ACK que recibio correctamente el paquete de FIN y se cierra la conexion.
Aclaracion:
cuando el servidor envia su FIN + ACK se queda esperando el ACK del cliente, si ese ACK se pierde, el servidor vuelve a enviar el FIN + ACK para que la conexion no quede colgada. Este loop es controlado por el kernel por lo tanto no habra reintentos infinitos, en algun momento los deja de mandar

Si sucede una desconexion abrupta se envia un paquete con RST que lo que hace es descartar todo lo que queda en el buffer por ver y destruye inmediatamente el socket y el socket lanza una exepcion. No se genera nningun ACK.

# 4)
Lo que hace `echo_tcp_server.py` 
Crea un socket que escucha cualquier host que se conecte al puerto 65432.
Y queda esperando una conexion.
Una vez se realiza una conexion recibe hasta 1024 bytes, toma esos bytes y lo retransmite al cliente pero transformando su contenido a mayusculas

Lo que hace `echo_tcp_client.py`
Crea un socket  y se conecta por localhost al puerto 65432.
Una vez se conecta al server tcp envia la cadena Hello world en bytes y se queda esperando a recibir hasta 1024 bytes que mandara el servidor.