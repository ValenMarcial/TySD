## 1)
### a)
Primero para crear la red debemos encender la configuracion de kathara
```bash
kathara check
kathara lstart
```
Dentro de la primer pc ejecutamos:
```bash
ip addr add 192.168.1.10/24 dev eth0
```
ahi creamos una red en pc1, en donde esta el 10 no se puede usar ni 0 ni 255 por que son direcciones reservadas.
Debemos hacer lo mismo para pc2 por con distinto numero a 10 por que si no tenemos varias pc con la misma direccion y una simula ser la otra.
```bash
ip addr add 192.168.1.20/24 dev eth0
```
como usamos kathara la tarjeta de red ya viene en estado up pero si usaramos virtualbox o VMware deberiamos hacer:
```bash
ip addr add 192.168.1.10/24 dev eth0
ip link set dev eth0 up
```
el `dev eth0` significa `device eth0` y seria el dispositivo `eth0` que es la tarjeta de red.

### b)
Al hacer ping las maquinas son alcanzables hacia ambos lados.

### c)
Primero se hizo un broadcast para encontrar la red `192.168.1.10`
![[Pasted image 20260914225837.png]]
Despues pc1 recibio un paquete para avisarle a pc2 que pc1 es la dueña de la ip y pueda enviarle los paquetes del ping.
La tabla ARP es una tabla con las traducciones de las redes locales para una comunicacion mas rapida y no tener que hacer un broadcast en cada paquete pero, si esa ip fuese externa se va directamente por el gateway del router para que el mismo se encargue de sacar el paquete fuera de la red local
### d)
Al hacer `arp` en cada pc una muestra la ip de la otra por que estan las ip cacheadas de la comunicacion anterior del ping. Se pueden ver tambien con `ip neigh show`

## 2)
Para limpiar las tablas de cache ARP podemos hacer:
```bash
ip neigh flush all
```
o para borrar una en especifico:
```bash
ip neigh del 192.168.1.x dev eth0
```
creamos en la pc2 el paquete IP:
```bash
scapy
paquete = IP(dst='192.168.1.10') / ICMP() / "Ejercicio 2 Prueba"
```
![[Pasted image 20260914233022.png]]

Primero se hizo un Broadcast como en el caso anterior y scapy usa una parte de su buffer para rellenar el paquete de broadcast que tiene que pesar 60 bytes y como le faltan 18 usa su propia memoria y mete cosas de un paquete anterior ahi para poder enviarlo. ESto en Linux no va a pasar por que se rellena con ceros. Despues mando por ICMP() el mensaje y luego se envio el broadcast a la pc2.
Con tcpdump:
![[Pasted image 20260914235303.png]]
- **El primer paquete (ARP Request):** Si miras la MAC de origen, dice `00:00:00:00:00:02`. Esa es la **PC2**. Fue la PC2 la que hizo el Broadcast preguntando por la `.10`. Como Scapy estaba corriendo ahí, rellenó el paquete con el texto viejo ("Paquete de prueba").
    
- **El paquete ICMP (El tercero en la lista):** Fíjate bien en las IPs de esa línea. Dice `192.168.1.20 > 192.168.1.10: ICMP echo request`. El origen (source) es la PC2. Esto confirma al 100% que el paquete con el texto "Prueba tcpdump" salió desde la PC2 hacia la PC1.
    
- **El rebote de la PC1 (El cuarto paquete):** Al recibir el ping, el sistema operativo de la PC1 responde automáticamente con un `ICMP echo reply`. Por regla del protocolo Ping, la máquina que responde **está obligada a devolver exactamente la misma carga de datos que recibió**. Por eso la PC1 le devuelve la frase "Prueba tcpdump" a la PC2.
    
- **El último paquete (ARP Reply):** Cinco segundos después, la PC1 necesita verificar la MAC de la PC2, así que envía un ARP Request (paquete 5). La **PC2** le responde (paquete 6). Como la PC2 es la que tiene Scapy y la memoria residual del ping anterior, rellena su respuesta ARP con "Prueba tcpdump".

## 3)

### a)
La ruta fisica desde A a F es A -> S1 -> S2 -> S4 -> S5 -> F
<div align="center"><strong>S1</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#1 & 4 & 0 & 6 & 2 \\ \hline
  \end{array}
$$

<div align="center"><strong>S2</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#1 & 6 & 0 & 4 & 1 \\ \hline
  \end{array}
$$

<div align="center"><strong>S4</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#1 & 4 & 3 & 8 & 2 \\ \hline
  \end{array}
$$

<div align="center"><strong>S5</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#1 & 8 & 0 & 5 & 1 \\ \hline
  \end{array}
$$

### b)
La ruta fisica de B a D es B -> S3 -> S1 -> S2 -> D

<div align="center"><strong>S3</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  B-D & 4 & 0 & 8 & 2 \\ \hline
  \end{array}
$$

<div align="center"><strong>S1</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  B-D & 8 & 1 & 7 & 2 \\ \hline
  \end{array}
$$

<div align="center"><strong>S2</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  B-D & 7 & 0 & 8 & 2 \\ \hline
  \end{array}
$$

### c)
Un camino mas corto entre A y E, para no saturar S1 Y S2 elegimos pasar por S3 pero hay dos posibles caminos con la misma cantidad de saltos:
A -> S1 -> S3 -> S4 -> E
A -> S1 -> S2 -> S4 -> E
Al ser un circuito que recién se está estableciendo (fase de _setup_), los switches deben negociar y reservar VCIs que estén "libres" en esos puertos. Como el enunciado no proveía los números para esta ruta, era necesario inventar un conjunto de VCIs (10,11,12,13)
<div align="center"><strong>S1</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-E & 10 & 0 & 11 & 1 \\ \hline
  \end{array}
$$

<div align="center"><strong>S3</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-E & 11 & 3 & 12 & 1 \\ \hline
  \end{array}
$$

<div align="center"><strong>S4</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-E & 12 & 3 & 13 & 1 \\ \hline
  \end{array}
$$

### d)
Una segunda ruta fisica desde A a F es A -> S1 -> S3 -> S4 -> S5 -> F como en el caso anterior hay que crear nuevos VCIs para no tener colisiones con los demas
<div align="center"><strong>S1</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#2 & 15 & 0 & 16 & 1 \\ \hline
  \end{array}
$$

<div align="center"><strong>S3</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#2 & 16 & 3 & 17 & 2 \\ \hline
  \end{array}
$$

<div align="center"><strong>S4</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#2 & 17 & 0 & 18 & 2 \\ \hline
  \end{array}
$$

<div align="center"><strong>S5</strong></div>
$$
\begin{array}{ |c|c|c|c|c| }
  \hline
  Conexion & \textbf{$VCI_{in}$} & \textbf{$port_{in}$} & \textbf{$VCI_{out}$} & \textbf{$port_{out}$} \\ \hline
  A-F\#2 & 18 & 0 & 19 & 1 \\ \hline
  \end{array}
$$
