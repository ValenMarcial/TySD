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

## 4)
### 1)
Tengo un route con 3 interfaces
eth0 -> Conectada al ISP (WAN) y la IP  es 200.71.49.56 
El router del ISP tiene IP 200.71.49.1

Se requiere configurar dos redes internas A y B con direcciones priovadas, cada red no va tener mas de 253 hosts cada una 
eth1 -> A
eth2 -> B

![[DiagramaRedFisica.excalidraw]]

### 2)
Como dice el enunciado cada subred tiene 253 hosts por lo tanto usa una mascara con /24 que serian 8 bits de host por lo tanto usa la mascara 255.255.255.0

Para subdividir la red deberia elegir 192.168.x.0/24

Verificamos que /24 alcanza para 253 hosts
Con mascara 255.255.255.0 quie es el /24
- Direcciones totales de 0 a 255
- Direccion de la red: 192.168.10.0 no se asigna a host
- Direccion de broadcast: 192.168.10.255 no se asigna a host
- Direcciones usables .1 a .254
- De esas 254 redes una se usa para el gateway de la subred y quedan 253

Ahora asignamos las redes
$$
\begin{array}{ |c|c|c|c| }
  \hline
  Interfaz & Red & ip asignada & Rol \\ \hline
   eth0 & 200.71.49.1 & 200.71.49.56 & \textbf{Asignada por el ISP} \\ \hline
   eth1 & 192.168.10.0 & 192.168.10.1/24 & \textbf{Gateway Subred A} \\ \hline
   eth2 & 192.168.20.0 & 192.168.20.1/24 & \textbf{Gateway Subred B} \\ \hline
  \end{array}
$$

Ahora las direcciones para los host de la subred A son:
192.168.10.2
192.168.10.3
192.168.10.4
192.168.10.5
...
192.168.10.254

Y las direcciones para los host de la subred B son:
192.168.20.2
192.168.20.3
192.168.20.4
192.168.20.5
...
192.168.20.254

no es necesario que cada host le siga la sucesiva puede tener H1 la 2 y H2 la 15 no importa el orden

![[DiagramaRedFisicaConIps.excalidraw]]

### 3)
#### a) Los host de ambas sub redes pueden comunicarse
La tabla de ruteo del router es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & Gateway & Interfaz \\ \hline
	200.71.49.0 & 255.255.255.0& 0.0.0.0 & eth0 \\ \hline
    192.168.10.0 & 255.255.255.0 & 0.0.0.0 & eth1 \\ \hline
    192.168.20.0 & 255.255.255.0 & 0.0.0.0 & eth2 \\ \hline
	0.0.0.0(internet) & 0.0.0.0 & 200.71.49.1 & eth0 \\ \hline	
  \end{array}
$$

La tabla de ruteo de un host de A es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    192.168.10.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
    0.0.0.0(default) & 0.0.0.0 & 192.168.10.1 & eth0 \\ \hline
  \end{array}
$$

La tabla de ruteo de un host de B es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    192.168.20.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
    0.0.0.0(default) & 0.0.0.0 & 192.168.20.1 & eth0 \\ \hline
  \end{array}
$$

#### b) Los hosts de ambas subredes no deben comunicarse
El router tiene ambas redes conectadas y se puede hacer de dos formas:

##### Primera forma:
Colocar la redireccion en las tablas de ruteo:
La tabla de ruteo del router es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & Gateway & Interfaz \\ \hline
	200.71.49.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
    192.168.10.0 & 255.255.255.0 & 0.0.0.0 & eth1 \\ \hline
    192.168.20.0 & 255.255.255.0 & 0.0.0.0 & eth2 \\ \hline
	0.0.0.0(internet) & 0.0.0.0 & 200.71.49.1 & eth0 \\ \hline	
  \end{array}
$$

La tabla de ruteo de un host de A es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    192.168.10.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
	192.168.20.0 & 255.255.255.0 & 0.0.0.0 & \text{lo o Null0}  \\ \hline
    0.0.0.0(default) & 0.0.0.0 & 192.168.10.1 & eth0 \\ \hline
  \end{array}
$$

La tabla de ruteo de un host de B es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    192.168.20.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
	192.168.10.0 & 255.255.255.0 & 0.0.0.0 & \text{lo o Null0} \\ \hline
    0.0.0.0(default) & 0.0.0.0 & 192.168.20.1 & eth0 \\ \hline
  \end{array}
$$

##### Segunda forma:
La otra forma es que hay que agregar una regla de filtrado en el router
Las tablas de ruteo quedan iguales y lo que hacemos es agregar reglas de forwarding con el comando iptables
```bash
iptables -A FORWARD -s 192.168.10.0/24 -d 192.168.20.0/24 -j DROP
iptables -A FORWARD -s 192.168.20.0/24 -d 192.168.10.0/24 -j DROP
```
Esato le dice al router sabes el camino pero no reenvies paquetes que vayan de A a B ni de B a A

#### c)Los host de la subred A pueden alcanzar solo a un dispositivo de la red B. Este dispositicco deberia acceder a cualquier host de A Y B
Hay dos formas:
##### Primera forma:
La tabla de ruteo del router es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & Gateway & Interfaz \\ \hline
	200.71.49.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
    192.168.10.0 & 255.255.255.0 & 0.0.0.0 & eth1 \\ \hline
    192.168.20.0 & 255.255.255.0 & 0.0.0.0 & eth2 \\ \hline
	0.0.0.0(internet) & 0.0.0.0 & 200.71.49.1 & eth0 \\ \hline	
  \end{array}
$$

La tabla de ruteo de un host de A es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    192.168.10.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
	192.168.20.50 & 255.255.255.255 & 192.168.10.1 & eth0 \\ \hline
	192.168.20.0 & 255.255.255.0 & DROP & \text{L0 o Null0}  \\ \hline
    0.0.0.0(default) & 0.0.0.0 & 192.168.10.1 & eth0 \\ \hline
  \end{array}
$$
La tabla de la impresora en la sub red B:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
	192.168.20.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
    0.0.0.0(default) & 0.0.0.0 & 192.168.20.1 & eth0 \\ \hline
  \end{array}
$$

La tabla de ruteo de los demas host de B son:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    192.168.20.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
	192.168.10.0 & 255.255.255.0 & DROP & \text{L0 o Null0} \\ \hline
    0.0.0.0(default) & 0.0.0.0 & 192.168.20.1 & eth0 \\ \hline
  \end{array}
$$

##### Segunda Forma:
Sin tocar las tablas de ruteo:
Lo que hacemos por ejemplo para conectar con una impresora que esta en la direccion 192.168.20.50 es
```bash
iptables -A FORWARD -s 192.168.10.0/24 -d 192.168.20.50 -j ACCEPT
iptables -A FORWARD -s 192.168.10.0/24 -d 192.168.20.0/24 -j DROP
```
Con esto bloqueamos todo lo que va de A a cualquier otra ip de B que no sea 192.168.20.50

## 5)
![[Pasted image 20260922204306.png]]

### a)
La tabla de ruteo de H1 es:
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    128.96.34.0 & 255.255.255.128 & 0.0.0.0 & eth0 \\ \hline
	0.0.0.0 & 0.0.0.0 & 128.96.34.1 & eth0 \\ \hline
  \end{array}
$$
Tabla de ruteo de R1, suponemos que eth0 esta conectado a 128.96.34.1 y eth1 a 128.96.34.130
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    128.96.34.128 & 255.255.255.128 & 0.0.0.0 & eth1 \\ \hline
    128.96.34.0 & 255.255.255.128 & 0.0.0.0 & eth0 \\ \hline
	128.96.33.0 & 255.255.255.0 & 128.96.34.129 & eth1 \\ \hline
  \end{array}
$$

Tabla de ruteo de R2, suponemos que eth0 esta conectado a 128.96.34.129 y eth1 a 128.96.33.1
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    128.96.34.128 & 255.255.255.128 & 0.0.0.0 & eth0 \\ \hline
	128.96.34.0 & 255.255.255.128 & 128.96.34.130 & eth0 \\ \hline
	128.96.33.0 & 255.255.255.0 & 0.0.0.0 & eth1 \\ \hline
  \end{array}
$$

Tabla de ruteo de H2
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
	128.96.34.128 & 255.255.255.128 & 0.0.0.0 & eth0 \\ \hline
	128.96.34.0 & 255.255.255.128 & 128.96.34.130 & eth0 \\ \hline
	128.96.33.0 & 255.255.255.0 & 128.96.34.129 & eth0 \\ \hline
  \end{array}
$$

Tabla de ruteo de H3
$$
\begin{array}{ |c|c|c|c| }
  \hline
   Destino & Mascara & GateWay & Interfaz \\ \hline
    128.96.33.0 & 255.255.255.0 & 0.0.0.0 & eth0 \\ \hline
    0.0.0.0 & 0.0.0.0 & 128.96.33.1 & eth0 \\ \hline
  \end{array}
$$

### b)
- **Envio**: H1 envia el paquete con destino `128.96.34.129` 
	- H1 lee la fila de la red de arriba (Destino `128.96.34.0`, Máscara `255.255.255.128`) y hace la operación AND.
	    - `128.96.34.139` AND `255.255.255.128`.
	        
	    - Evaluando el último octeto en binario: `10001011` (139) AND `10000000` (128) = `10000000` (que es 128 en decimal).
	        
	    - El resultado es la subred `128.96.34.128`. Como esto **no coincide** con el destino de la regla (`128.96.34.0`), H1 descarta esta fila.
    - Luego:
	    - H1 lee la siguiente fila(Destino `0.0.0.0`, Máscara `0.0.0.0`) y repite la operación AND.
	    
	    - El resultado es logicamente `0.0.0.0` ya que se fue por el caso de destino default asi que coincide y es enviado fuera de la red hacia el gateway `128.96.34.1` por la interfaz `eth0` de H1. 
        
- **Recepción:** R1 recibe el paquete en su interfaz `eth0` con la IP de destino `128.96.34.139`.
	- **Evaluación de la primera regla:** R1 lee la fila de la red de arriba (Destino `128.96.34.0`, Máscara `255.255.255.128`) y hace la operación AND.
	    - `128.96.34.139` AND `255.255.255.128`.
	    - Evaluando el último octeto en binario: `10001011` (139) AND `10000000` (128) = `10000000` (que es 128 en decimal).
	    - El resultado es la subred `128.96.34.128`. Como esto **no coincide** con el destino de la regla (`128.96.34.0`), R1 descarta esta fila.
	- **Evaluación de la segunda regla:** R1 lee la fila de la red del medio (Destino `128.96.34.128`, Máscara `255.255.255.128`) y repite la operación AND.
	    - El resultado lógicamente vuelve a ser `128.96.34.128`.
	    - Esta vez, el resultado **sí coincide exactamente** con el destino configurado en la regla.   
- **Decisión de reenvío:** Al encontrar el "match", el router lee la columna de la interfaz correspondiente a esa fila, que es `eth1`.
- **Entrega final:** Como el Gateway de esa regla indica conexión directa (`0.0.0.0`), R1 sabe que H2 está conectado a ese mismo cable físico. Resuelve su dirección MAC y entrega el paquete directamente por `eth1`.

#### Explicacion de la entrega Final:
Cuando el paquete se envia por una conexion directa lo que pasa es que tiene que darselo directamente  al destino por lo tanto se hace una entrega mediante `ARP`:
- **Consulta interna:** R1 mira su memoria temporal (tabla ARP) para ver si ya tiene anotada la dirección MAC que le corresponde a la IP de H2 (`128.96.34.139`).
    
- **Petición ARP (Broadcast):** Si no la tiene registrada, R1 pausa el paquete un milisegundo y envía un mensaje de difusión por su puerto `eth1` que le llega a todos los dispositivos conectados a ese switch. El mensaje básicamente pregunta: _"¿Quién de ustedes tiene la IP `128.96.34.139`? Envíenme su dirección MAC"_.
    
- **Respuesta de H2:** Todos los equipos del segmento reciben el mensaje, pero lo ignoran. Solo H2 reconoce que es su propia IP, por lo que le responde directamente a R1: _"Yo soy esa IP, y mi dirección MAC es 00:1A:2B:3C:4D:5E"_.
    
- **Encapsulamiento:** R1 guarda esa información. Ahora toma el paquete IP original que venía desde H1, lo envuelve dentro de una estructura de nivel inferior llamada "Trama Ethernet", y le estampa como destino la dirección MAC que H2 le acaba de dar.
    
- **Transmisión física:** R1 empuja esta trama por su interfaz `eth1`. El switch de la red lee la dirección MAC y envía los impulsos eléctricos directamente por el cable que va hacia la computadora H2.