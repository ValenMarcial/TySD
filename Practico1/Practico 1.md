
# 1)
Para ver la ip local hay que hacer ip a o ip addr y buscar la linea que dice inet 192.xxx.xx.x yo ejecute 
```bash
ip a | grep 192
```

instale nmap y ejecute 
```bash
nmap -sn 192.168.3.114 #red local del laboratorio
```
```bash
#Como resultado obtuve
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-08-14 08:13 -03
Nmap scan report for vmarcial-IdeaPad-3-14ITL6 (192.168.3.114)
Host is up (0.000071s latency).
Nmap done: 1 IP address (1 host up) scanned in 0.14 seconds
```

# 2)
El servidor responde 200 ok en el paquete de styles osea el css y 200 en el index que es el html de la ruta de la pagina en al que estamos parados.
Y si recargamos la pagina  el servidor responde 304  ya que usa la cache del navegador y ahi esta cargado ya todo.

# 3)

Ejecutar una peticion desde consola con protocolo HTTP
```bash
nc example.net 80
GET / HTTP/1.1
Host: example.net
```
nc abre una conexión (generalmente TCP o UDP) hacia otra computadora, envía los datos que le pases y escupe en tu terminal lo que la otra computadora responda.

Ahora ejecutamos y cerramos la conexion
```bash
GET / HTTP/1.1
Host: example.net
Connection: close
```
Basicamente esto cierra la conexion por que nc mantiene una conexion (TCP/UDP) y eso es persistente entonces podemos enviar mas cosas y seguir viendo las respuestas de esa conexion.

## Experimento
Realizamos en dos consolas diferentes esto
```bash
nc -u -l 8080
```
esto abre el puerto 8080 en la red privada y queda escuchando con udp
En otra terminal hacemos
```bash
nc -u 127.0.0.1 8080
```
en la consola dos podemos escribir cualquier contenido y la consola uno lo va a recibir y lo va a mostrar, pero en la consola dos no llegara ninguna respuesta de la consola uno.

### Para TCP
No se puede ver con nc por que el manejo de comunicacion TCP se produce en el kernel y nc es un programa no es una llamada a sistema entonces tenemos que usar tres terminales para 
replicar el experimento
En la primer terminal vamos a escuchar la comunicacion con el puerto 8080 con tcpdump que sirve para mostrar los paquetes tcp que llegan a un puerto determinado
```bash
sudo tcpdump -i lo port 8080 -nn
```

En la segunda y tercer terminal levantamos las conexiones tcp con nc
```bash
nc -l 8080
```

```bash
nc 127.0.0.1 8080
```
Ahora cada vez que escribamos algo en la tercer consola se veran los paquetes tcp que llegan al sistema operativo y como se manejan, y en la segunda terminal se vera el contenido que mande desde la tercer terminal.

# 4)
```bash
traceroute google.com
traceroute to google.com (172.217.28.14), 30 hops max, 60 byte packets
 1  unifi.localdomain (192.168.3.1)  2.674 ms  3.387 ms  3.366 ms
 2  200.7.130.1 (200.7.130.1)  4.886 ms  4.867 ms  4.847 ms
 3  10.7.2.1 (10.7.2.1)  4.444 ms  4.804 ms  4.785 ms
```

Lo que sucede es que primero se hace la peticion desde el router que esta conectada mi computadora (192.168.3.1) se conecta a la red publica de la universidad de rio cuarto (200.7.130.1) esa peticion se manda a la red privada (10.7.2.1) que se termina conectando despues de varios saltos que traceroute omite pero finalmente se conecta con un servidor de google (172.217.28.14).

# 5)
>[!NOTE]   Tabla de anchos de banda y atenuación soportados por los siguientes medios:
1. UTP categoría 3 (telefónico)
2. UTP categoría 5 o 6 (Ethernet)
3. Cable coaxial
4. Fibra óptica

| *Medio de Transmisión*            | *Ancho de Banda Máximo (Frecuencia / Velocidad)*                                  | *Atenuación Típica*                                                               | *Notas clave para apuntes*                                                                                 |
| --------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| *UTP Categoría 3* (Telefónico)    | Hasta 16 MHz (Soporta 10 Mbps)                                                    | *~43 dB / 100m* (medido a 16 MHz)                                                 | Obsoleto para datos; usado históricamente para telefonía y redes antiguas (10BASE-T).                      |
| *UTP Categoría 5e / 6* (Ethernet) | Cat 5e: 100 MHz (1 Gbps)<br><br>  <br>  <br><br>Cat 6: 250 MHz (1 Gbps - 10 Gbps) | *~20 a 22 dB / 100m* (medido a 100 MHz)                                           | Estándar LAN actual. El límite práctico de distancia por atenuación son 100 metros.                        |
| *Cable Coaxial*                   | 500 MHz a >1 GHz (Multi-Gigabit)                                                  | *~8.9 dB / 100m* (a 100 MHz)<br><br>  <br>  <br><br>*~21.6 dB / 100m* (a 500 MHz) | Menor atenuación que el UTP a altas frecuencias por su excelente blindaje de interferencias.               |
| *Fibra Óptica*                    | Multi-Tbps (rango de los TeraHertz)                                               | *Monomodo:* ~0.2 dB / *km*<br><br>  <br>  <br><br>*Multimodo:* ~3 dB / *km*       | ¡Ojo a la unidad! La atenuación es tan baja que se mide por *kilómetro*. Inmune al ruido electromagnético. |


# 6)

Ancho de banda 3Khz sin ruido
Cuantos bps se pueden transmitir como máximo en una señal digital de 4 niveles discretos

Tasa máxima de transmisión $2*B*\log_{2}(V)$ donde
$B=3\text{Khz}$
$V=4$
Pero antes hay que pasar los $3\text{KHz}$ a $Hz$ que esto se hace $3 * 1000 = 3000\text{Hz}$
entonces $\text{Tasa maxima de Transmision} = 2*3000*\log_2(4) = 12000\text{bps}$

# 7)

Queremos obtener una tasa de transmisión de $24Kbps$ 
En un canal sin ruido con $4KHz$ de ancho de banda
entonces
$$
\begin{aligned}
& (4*1000) * 2 * \log_{2}(V) = (24 * 1000) \\
& 8000 * \log_{2}(V) = 24000 \\
& \log_{2}(V) = 3 \\
& V = 2³ \\
& V = 8
\end{aligned}
$$
Con esto obtenemos que la cantidad de valores discretos debe ser $8$

# 8)
Capacidad máxima del canal es
$B * \log_{2}(1+SNR)$ 

en este caso
$$
\begin{aligned}
& B = 3000Hz \\
& SNR = \frac{S}{N} \\
& 
\end{aligned}
$$
Como sabemos que $10*\log_{10}\left( \frac{S}{N} \right) = 20\text{Db}$
entonces
$$
\begin{aligned}
& S = 10^{2} * N \\
\end{aligned}
$$
Por lo tanto 
$$
\begin{aligned}
& SNR = \frac{10^{2} * N}{N} \\
& SNR = 10^{2} \\
& SNR = 100 \\
\end{aligned}

$$
Entonces :
$$
\begin{aligned}
& \text{Capacidad Maxima Del Canal}  = 3000 * \log_{2}(101) \approx 19974.6 \text{bps}
\end{aligned}
$$

# 9)
$\text{Altitud } 35,786 \text{ km}$ sobre la superficie terrestre
La señal viaja en el vacío por lo tanto <b>no tiene ruido</b>, y va a la velocidad de la luz $c = 300000 \text{ km/s}$

## a)
Tiempo de propagación de ida desde la estación hasta el satélite.
$$
\begin{aligned}
& t = \frac{d}{v} \\
& t = \frac{35,786}{300000} \\
& t \approx 0.119 \\
\end{aligned}
$$
Entonces desde la estacion al satelite el tiempo de propagacion es:
$$
\begin{aligned}
& 0.119 \text{ s} = 119 \text{ ms}
\end{aligned}

$$

## b)


Hay dos formas de calcular la latencia mínima de ida y vuelta RTT

### Caso A: Enlace directo punto a punto (2 tramos)
Si el destino final del paquete es el propio satélite (o una estación que recibe directamente en el mismo haz):

$$\text{RTT} = 2 * t_{\text{prop}} = 2 * 119\text{ ms} \approx \mathbf{238\text{ ms}}$$

### Caso B: Enlace satelital de Internet tradicional (4 tramos / Doble salto)
En una conexión típica de Internet satelital (como GEO tradicional / VSAT), el paquete de solicitud debe subir al satélite y bajar a la estación terrestre/telepuerto (Gateway conectado a Internet), y la respuesta debe hacer el mismo camino inverso:

1. *Subida:* Usuario $\rightarrow$ Satélite ($119\text{ ms}$)

2. *Bajada:* Satélite $\rightarrow$ Telepuerto / Servidor ($119\text{ ms}$)

3. *Subida (Respuesta):* Telepuerto $\rightarrow$ Satélite ($119\text{ ms}$)

4. *Bajada (Respuesta):* Satélite $\rightarrow$ Usuario ($119\text{ ms}$)


$$\text{Distancia total recorrida} = 4 \cdot 35.786\text{ km} = 143.144\text{ km}$$

$$\text{RTT}{\text{mínimo}} = 4 \cdot t{\text{prop}} = 4 \cdot 119\text{ ms} \approx \mathbf{476\text{ ms}}$$

### Resumen

- *Propagación de ida (1 tramo):* *$\approx 119\text{ ms}$*
- *RTT directo (2 tramos):* *$\approx 238\text{ ms}$*    
- *RTT en servicio de Internet comercial (4 tramos):* *$\approx 476\text{ ms}$* (en la práctica ronda los ~500–600 ms al sumar el procesamiento y la red terrestre).

$$\text{RTT} = 4 \cdot 119\text{ ms}$$


