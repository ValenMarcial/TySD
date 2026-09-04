Laboratorio: Dos computadoras conectadas directamente
=====================================================

En este laboratorio vamos a crear una red con dos computadoras conectadas
directamente (sin uso de switches).

Requerimientos
--------------

Kathara, el cual requiere un docker daemon corriendo.

Para verificar que kathara puede correr en su computadora, ejecutar

    kathara check

El archivo de configuración de kathara (lab.conf)
-------------------------------------------------

    LAB_DESCRIPTION="Two computers with a direct link between its interfaces"
    LAB_VERSION=1.0
    LAB_AUTHOR="Sistemas Distribuidos - UNRC"
    LAB_EMAIL=contact@kathara.org
    LAB_WEB=http://www.kathara.org/

    pc1[0]="A/00:00:00:00:00:01"
    pc1[image]="kathara/base"
    pc1[ipv6]="false"

    pc2[0]="A/00:00:00:00:00:02"
    pc2[image]="kathara/base"
    pc2[ipv6]="false"

    wireshark[bridged]=true
    wireshark[port]="3000:3000"
    wireshark[image]="lscr.io/linuxserver/wireshark"
    wireshark[num_terms]=0

Este archivo define dos computadoras en una red (dominio) denominada `A`.
Cada pc tiene una interface de red (Ethernet) con direcciones dadas.
Cada interface se verá como el dispositivo de red 'eth0' en cada pc virtual.

La última sección lanza el servidor de Wireshark que actúa como un *sniffer* de
la red, capturando los paquetes transmitidos.
Sirve una interfaz web al que se puede acceder vía un browser con el url
'http://localhost:3000/'.

Ejecución de las máquinas (pc1 y pc2)
-------------------------------------

En la carpeta del laboratorio (donde descomprimió los archivos) hacer:

    kathara lstart

Kathara lanzará por cada computadora una imagen Docker con un usuario root,
interfaces de red virtuales, una imagen del sistema de archivos con un conjunto
de aplicaciones para configurar la red y realizar experimentos, incluyendo el
comando `ip` (para configurar IP), `scapy` y otras utilidades.

Por cada computadora, kathara lanza una terminal (xterm por omisión) y un shell.

Configurar kathara para usar wireshark
--------------------------------------

Wireshark permite interceptar (sniffing) los paquetes de red.
En este escenario se requiere que kathara configure el daemon de wireshark
para que se ubique como un host (computadora) conectado al enlace entre las dos
pcs. En la terminal del host (donde se ejecutó `kathara lstart`), hacer:

    kathara lconfig -n wireshark --add A

Esto dispara un host virtual con dos interfaces:
 - eth0: Escucha el servidor de wireshark.
 - eth1: Se conecta al enlace entre las dos pcs en la red `A`.

Abajo se muestra el esquema de la red creada.

     +-------+ eth0                   eth0 +-------+
     |  pc1  |-----------------------------|  pc2  |
     +-------+             |               +-------+
                           |eth1
                     +-----------+
                     | wireshark |
                     +-----------+
                           |eth0 (bridge to host)
                           |
                http://localhost:3000/

Experimentando con kathara, Scapy y wireshark
---------------------------------------------

1. En cada pc, hacer ifconfig. Debería observar que eth0 no ha recibido
   paquetes.
2. En un browser conectarse con wireshark: Al URL `http://localhost:3000/` y
   seleccionar la interface `eth1` para comenzar la captura.
2. Lanzar Scapy en la `pc1` ejecutando el comando `scapy`. Esto lanza un
   intérprete sobre Python para ejecutar comandos de *scapy*.
3. Crear y enviar un paquete Ethernet desde `pc1` a `pc2`:

   ```
   >>> p = Ether(dst='00:00:00:00:00:02', src='00:00:00:00:00:01') / Raw(load="Hello world")
   >>> sendp(p, iface="eth0")
   ```

4. Verificar, con `ifconfig`, que se ha recibido un paquete en la `pc2`.
5. Analizar el paquete interceptado por Wireshark.
6. Enviar otro paquete Ethernet con el valor del campo `type=0x0800` (IP) y
   observar el paquete interceptado por Wireshark.

Capturando tráfico con `tcpdump`
--------------------------------

Nota: También es posible capturar los paquetes sin usar `wireshark` usando el
comando `tcpdump`.

En la `pc2` ejecutar

`tcpdump -i eth0 -e -nn -X`

y en la `pc1` enviar nuevamente el frame Ethernet.

_Nota_: Hacer `man tcpdump` para más detalles sobre su uso.

Finalizar la red
----------------

Ejecutar en la terminal del _host_ (donde se lanzó los comandos `kathara`) el
comando `kathara lclean` finaliza los contenedores simulando los dispositivos
creados.

El comando `kathara wipe` elimina todos los dispositivos virtuales creados por
kathara.

