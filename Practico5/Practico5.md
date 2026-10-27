# 1)
## a)
```bash
dig dc.exa.unrc.edu.ar

; <<>> DiG 9.20.24-1ubuntu0.4-Ubuntu <<>> dc.exa.unrc.edu.ar
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47195
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;dc.exa.unrc.edu.ar.		IN	A

;; ANSWER SECTION:
dc.exa.unrc.edu.ar.	3600	IN	A	200.7.141.44

;; Query time: 35 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Sun Oct 25 22:59:16 -03 2026
;; MSG SIZE  rcvd: 63

```
El resultado nos muestra la ip publica `200.7.141.44` que corresponde a una ip clase C

## b)
```bash
dig NS dc.exa.unrc.edu.ar

; <<>> DiG 9.20.24-1ubuntu0.4-Ubuntu <<>> NS dc.exa.unrc.edu.ar
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61266
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;dc.exa.unrc.edu.ar.		IN	NS

;; ANSWER SECTION:
dc.exa.unrc.edu.ar.	3600	IN	NS	reunirc2.unrc.edu.ar.
dc.exa.unrc.edu.ar.	3600	IN	NS	reunirc3.unrc.edu.ar.
dc.exa.unrc.edu.ar.	3600	IN	NS	reunirc.unrc.edu.ar.

;; Query time: 25 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Mon Oct 26 12:28:16 -03 2026
;; MSG SIZE  rcvd: 115

```

Los servidores de nombres son 
;; ANSWER SECTION:
dc.exa.unrc.edu.ar.	3600	IN	NS	`reunirc2.unrc.edu.ar.`
dc.exa.unrc.edu.ar.	3600	IN	NS	`reunirc3.unrc.edu.ar.`
dc.exa.unrc.edu.ar.	3600	IN	NS	`reunirc.unrc.edu.ar.`

Estos no tienen orden jerarquico, no prioridad asignada, siempre estan sincronizados para que todos los nodos contengan la misma informacion,.
Los criterios de eleccion de DNS son:
- **Medición de latencia (RTT - Round Trip Time):** El resolver le pregunta al servidor que le responda más rápido en ese momento. Si `reunirc2` responde en 10 ms y `reunirc` en 30 ms, elegirá `reunirc2`.
    
- **Balanceo de carga (Round-Robin):** Muchos sistemas van rotando las peticiones entre los tres para distribuir el tráfico y evitar que un solo servidor procese todas las consultas.
    
- **Tolerancia a fallos (Alta disponibilidad):** Si el servidor elegido no responde (por caída de red, mantenimiento o falla de software), el resolver pasa **inmediatamente** a consultar a cualquiera de los otros dos disponibles.
## c)
Para consultar los servidores de mail usamos
```bash
dig MX dc.exa.unrc.edu.ar

; <<>> DiG 9.20.24-1ubuntu0.4-Ubuntu <<>> MX dc.exa.unrc.edu.ar
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 62535
;; flags: qr rd ra; QUERY: 1, ANSWER: 7, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;dc.exa.unrc.edu.ar.		IN	MX

;; ANSWER SECTION:
dc.exa.unrc.edu.ar.	3600	IN	MX	20 ALT1.ASPMX.L.GOOGLE.COM.
dc.exa.unrc.edu.ar.	3600	IN	MX	10 ASPMX.L.GOOGLE.COM.
dc.exa.unrc.edu.ar.	3600	IN	MX	20 ALT2.ASPMX.L.GOOGLE.COM.
dc.exa.unrc.edu.ar.	3600	IN	MX	30 ASPMX4.GOOGLEMAIL.COM.
dc.exa.unrc.edu.ar.	3600	IN	MX	30 ASPMX3.GOOGLEMAIL.COM.
dc.exa.unrc.edu.ar.	3600	IN	MX	30 ASPMX2.GOOGLEMAIL.COM.
dc.exa.unrc.edu.ar.	3600	IN	MX	30 ASPMX5.GOOGLEMAIL.COM.

;; Query time: 35 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Mon Oct 26 12:35:42 -03 2026
;; MSG SIZE  rcvd: 226
```

Donde se eligen por prioridad osea el que prioridad mas chica tenga va ser el primero en salir elegido.
dc.exa.unrc.edu.ar.	3600	IN	MX	20 `ALT1.ASPMX.L.GOOGLE.COM.`
dc.exa.unrc.edu.ar.	3600	IN	MX	10 `ASPMX.L.GOOGLE.COM.`
dc.exa.unrc.edu.ar.	3600	IN	MX	20 `ALT2.ASPMX.L.GOOGLE.COM.`
dc.exa.unrc.edu.ar.	3600	IN	MX	30 `ASPMX4.GOOGLEMAIL.COM.`
dc.exa.unrc.edu.ar.	3600	IN	MX	30 `ASPMX3.GOOGLEMAIL.COM.`
dc.exa.unrc.edu.ar.	3600	IN	MX	30 `ASPMX2.GOOGLEMAIL.COM.`
dc.exa.unrc.edu.ar.	3600	IN	MX	30 `ASPMX5.GOOGLEMAIL.COM.`

por ejemplo el primero en ser elegido es el de prioridad 10, y en este caso el primer MX y el tercero tienen la misma prioridad osea que si se deberia elegir entre ellos por que son la prioridad mas alta se elige con estos criterios:

 1. **Selección / Balanceo de carga:** El servidor que envía el correo elige uno de los servidores con la misma prioridad de forma aleatoria o rotativa (_round-robin_) para distribuir el tráfico de manera uniforme entre ellos.
    
2. **Reintento inmediato:** Si el servidor elegido no responde o rechaza la conexión, el emisor no falla la entrega; intenta conectarse inmediatamente al otro servidor de esa **misma** prioridad.
    
3. **Escalado por prioridades:** El emisor solo intentará entregar el correo a un servidor con menor preferencia (número de prioridad más alto, como `20` o `30`) si **todos** los servidores del nivel prioritario más bajo (los de valor `10`) no están disponibles.
## d) 
Al final de cualquier consulta con dig aparece la ip del dns local, en este caso es:
;; SERVER: 127.0.0.53#53(`127.0.0.53`) (UDP)

# 2)
```bash
nc www.example.com 80
GET / HTTP/1.1
Host: www.example.com
Connection: close
```

Ya que /index.html no funcionaba asi pude devolver el contenido de la pagina principal de www.example.com

Con el navegador apretando `f12` y entrando a la seccion `Network` marcando la casilla `Disable Cache` y haciendo `CTRL + SHIFT + R` recargamos y logramos que devuelva el 200 ok de los recursos usados por http://www.example.com
![[Pasted image 20261026132601.png]]

1. **La naturaleza "en cascada" de la Web:** Un usuario piensa que "carga una página", pero en realidad el navegador realiza **múltiples peticiones HTTP independientes**. `netcat` te muestra únicamente la petición que le pides explícitamente (solo el HTML), mientras que el navegador parsea ese texto y dispara de forma automática solicitudes secundarias para descargar sus dependencias (como el código JavaScript `s.js` o las reglas de estilo `content.css`).
    
2. **HTTP como protocolo de texto plano sobre TCP:** Al usar `netcat`, estás abriendo un socket TCP crudo y comunicándote en el protocolo de aplicación directo. Te demuestra que HTTP no tiene magia: son simplemente líneas de texto (`GET`, `Host`, `HTTP/1.1 200 OK`) enviadas a través de una conexión TCP.
    
3. **La automatización y gestión de estado del cliente:** El navegador administra de forma transparente metadatos que tú no tuviste que escribir en `netcat`:
    
    - **Cabeceras automáticas:** Envía tu sistema operativo, versión del navegador (`User-Agent`), codificaciones soportadas (`Accept-Encoding`), etc.
        
    - **Gestión de caché:** Evalúa si el archivo ya existe en tu disco para evitar retransmisiones innecesarias, devolviendo respuestas como `304 Not Modified`.

# 3)

## a) 
Ejecutamos desde clock-app:
```bash
python3 http-server.py
```
ingresamos a `http://localhost:8080/` y aca veremos un reloj que nos va dando la hora haciendo peticiones http.

## c)
Basicamente para agregar el puerto del cliente, hay que mandarlo por la conexion tcp, cuando el http-server se conecta y el cliente accede a http://localohost:8080/ lo que sucede es que se crea una conexion TCP entre el cliente y el servidor, y el handler_class lo que hace es tomar el puerto del cliente que desde el servidor no se puede acceder pero al agregarlo en una de las clases manejadoras y agregar el metodo get_environ() donde agregamos al environ del servidor http el dato de puerto de cliente, ahi si logramos mostrar por JSON el puerto del cliente
1. **El cliente no manda el puerto como parte del contenido HTTP.** Al establecer la conexión TCP, el sistema operativo usa un puerto de origen y el servidor puede conocerlo desde el socket. En `wsgiref`, el handler accede a ese extremo mediante `self.client_address`.
2. **El puerto sí es accesible desde el servidor**, pero no necesariamente desde Bottle directamente. El handler lo copia al `environ` WSGI de esa solicitud con `get_environ()`. Entonces la ruta de Bottle puede leerlo y devolverlo como JSON.

El flujo queda así:
```txt
Conexión TCP: cliente:puerto_origen → servidor:8080
        ↓
handler obtiene el puerto de origen del socket
        ↓
lo agrega al environ WSGI de la solicitud
        ↓
Bottle lee el dato y responde con JSON
```

Al entrar a `http://localhost:8080/`, el puerto `8080` es el destino del servidor; el puerto de origen del cliente suele ser otro, asignado temporalmente.