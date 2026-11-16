# 1)
![[ejercici1p6.excalidraw]]

# 2)
Para pasar del orden parcial que ofrecen los relojes vectoriales a un orden total estricto de todos los eventos del sisteman, se usa una tecnica de resolucion de empates (tie-breaking) basada en las identidades fijas de los procesos

## Mecanismo para obtener un Orden Total $<_{total}$
Dfinimos una relacion de orden total entre dos eventos $x$ (ocurrido en $P_{i}$) y $y$ (ocurrido en $P_{j}$), con marcas de tiempo vectoriales $V(x)$ y $V(y)$. mediante el algoritmo de dos pasos
### 1) Orden causal Principal (Relacion de precedenccia vectorial)
Si $V(x) < V(y)$ entonces $x <_{total} y$ 
### 2) Desempate arbitrario (edeterminista) por id de proceso
Si $x$ e $y$ son concurrentes $(V(x) || V(y))$ rompemos el empate comparando los identificadores de los procesos $i$ y $j$ donde ocurrieron los eventos
- Si $V(x) || V(y) \implies x <_{total} y \Leftrightarrow i < j$ 

| **Evento** | **Proceso emisor** | **Marca vectorial V** |
| ---------- | ------------------ | --------------------- |
| **$a$**    | $P_1$              | $(1, 0, 0)$           |
| **$b$**    | $P_2$              | $(0, 1, 0)$           |
| **$c$**    | $P_3$              | $(0, 0, 1)$           |
| **$d$**    | $P_1$              | $(2, 0, 0)$           |
| **$e$**    | $P_2$              | $(2, 2, 0)$           |
| **$f$**    | $P_3$              | $(0, 0, 2)$           |
## Paso a paso
### Eventos a, b ,c concurrentes entre si
$V(a) = (1,0,0), V(b) = (0,1,0), V(c) = (0,0,1)$
ninguno domina vectorialmente al otro  ($a || b, b || c, a || c$)
Aplicamos desempate por identificador de procesos ($1<2<3$)
$a <_{total} b <_{total} c$

### Evento d en $P_{1}$
$V(d) = (2,0,0)$
comparado con $a: (1,0,0) < (2,0,0) \implies a <_{total} d$
comparado con $b$ en $P_{2}:V(b) = (0,1,0)$  y $V(d) = (2,0,0)$ son concurrentes
Como el proceso de $d$ es 1 y el de $b$ es 2, se cumple que $d <_{total} b$ por $1<2$

### Evento e en $P_{2}$
$V(e) = (2,2,0)$
Como $V(d) (2,0,0) < (2,2,0) = V(e)$, existe relacion causal explicita 
$d <_{total} e$

### Evento f en $P_{3}$
$V(f) = (0,0,2)$
$V(e) = (2,2,0)$ y $V(f) = (0,0,2)$ son concurrentes $e||f$
Desempate por id de proceso: $e$ ocurrio en $P_{2}$ y $f$ en $P_{3}$ como $2<3$
$e <_{total}f$

### Resultado del orden total final
$a <_{total} d <_{total} b <_{total} e <_{total} c <_{total} f$


# 3)
n procesos, cada proceso es un servidor,  hay que replicar una base de datos de pares con forma (clave, valor). Usa relojes logicos escalares

## Funcionamiento del Reloj Escalar
Cada proceso $P_i$ mantiene un único entero $L_i$, inicializado en $0$. Las reglas de actualización son:

1. Evento local o de envío:
   Antes de registrar un evento local o transmitir un mensaje, el proceso incrementa su contador:$$L_i \leftarrow L_i + 1$$
2. Envío de mensaje:
   Al enviar un mensaje $m$, el proceso adjunta su valor actual $L_i$ como marca de tiempo 
   ($T_m = L_i$).

3. Recepción de mensaje:
   Al recibir un mensaje con marca $T_m$, el proceso $P_i$ ajusta su reloj al máximo entre su reloj actual y el del mensaje, y luego lo incrementa en $+1$:$$L_i \leftarrow \max(L_i, T_m) + 1$$
   
## La Propiedad del Tiempo Relativo (Relación de Causalidad)
Los relojes escalares garantizan la condición de reloj:$$\text{Si un evento } a \text{ causó a } b \implies L(a) < L(b)$$Sin embargo, la implicación inversa no se cumple. Tener $L(a) < L(b)$ no significa que $a$ haya causado a $b$; los eventos podrían ser completamente independientes (concurrentes).

## Generación de un Orden Total con Relojes Escalares

Dado que dos eventos en procesos distintos pueden tener exactamente el mismo valor de reloj escalar (por ejemplo, $L(a) = 2$ y $L(b) = 2$), los relojes escalares solos generan un orden parcial.

Para transformarlo en un **orden total**, se aplica el desempate por la tupla $\langle L(x), \text{ID}_x \rangle$:

$$x <_{\text{total}} y \iff \Big(L(x) < L(y)\Big) \lor \Big(L(x) = L(y) \land \text{ID}_x < \text{ID}_y\Big)$$

Este mecanismo es ampliamente utilizado en algoritmos distribuidos como la **exclusión mutua distribuida de Lamport** o en sistemas de **difusión con orden total** (_Total Order Multicast_), ya que permite a todos los nodos acordar un único orden global con un gasto computacional y de red mínimo.

## Solucion
La **consistencia secuencial** exige que exista un orden global único para todas las operaciones (lecturas y escrituras) que sea respetado por todos los nodos, y que las operaciones de un mismo cliente se ejecuten en el orden programado por ese cliente.

Para ver con total claridad por qué el protocolo falla, analicemos paso a paso cómo se comportan las reglas y armemos un ejemplo sencillo con **2 réplicas ($R_1$ y $R_2$) y 2 clientes ($C_A$ y $C_B$)**.

### Las Reglas del Protocolo (para tener a mano)

1. **Lectura local:** Al leer, la réplica devuelve lo que tiene guardado en ese instante.
    
2. **Escritura local:** Al escribir, la réplica guarda el valor, hace $C_i = C_i + 1$ y envía un mensaje `update` a las demás.
    
3. **Recepción de update:** Al recibir `update(key, value), Cj`:
    
    - Si $C_j > C_i$: actualiza el valor y hace $C_i = C_j$.
        
    - Si $C_j \le C_i$: **descarta e ignora** el mensaje.
        

### Paso a paso del escenario

**Estado inicial:**

- Réplica $R_1$: Clave $k = \text{"v0"}$, Reloj $C_1 = 0$
    
- Réplica $R_2$: Clave $k = \text{"v0"}$, Reloj $C_2 = 0$
    

#### Paso 1: Cliente A escribe en $R_1$

El Cliente A envía `write(k, "vA")` a **$R_1$**.

- $R_1$ ejecuta la regla de escritura:
    
    1. Guarda $k = \text{"vA"}$.
        
    2. Incrementa su reloj: $C_1 = 0 + 1 = 1$.
        
    3. Envía por la red el mensaje `update(k, "vA"), Cj=1` hacia $R_2$.
        
- _(Por congestión de red, este mensaje de $R_1 \to R_2$ se demora en viajar)._
    

#### Paso 2: Cliente B escribe en $R_2$ al mismo tiempo

En simultáneo, el Cliente B envía `write(k, "vB")` a **$R_2$**.

- $R_2$ ejecuta la regla de escritura en su nodo:
    
    1. Guarda $k = \text{"vB"}$.
        
    2. Incrementa su reloj: $C_2 = 0 + 1 = 1$.
        
    3. Envía por la red el mensaje `update(k, "vB"), Cj=1` hacia $R_1$.
        

#### Paso 3: $R_1$ recibe la actualización de $R_2$

A $R_1$ le llega el mensaje `update(k, "vB"), Cj=1` que envió $R_2$.

- $R_1$ evalúa la condición del protocolo:
    
    - ¿Es $C_j > C_1$?
        
    - Sustituyendo valores: ¿Es $1 > 1$? **FALSO.**
        
- **Resultado en $R_1$:** Descarta el mensaje. $R_1$ mantiene $k = \text{"vA"}$ y $C_1 = 1$.
    

#### Paso 4: $R_2$ recibe la actualización de $R_1$

A $R_2$ le llega el mensaje `update(k, "vA"), Cj=1` que envió $R_1$.

- $R_2$ evalúa la condición del protocolo:
    
    - ¿Es $C_j > C_2$?
        
    - Sustituyendo valores: ¿Es $1 > 1$? **FALSO.**
        
- **Resultado en $R_2$:** Descarta el mensaje. $R_2$ mantiene $k = \text{"vB"}$ y $C_2 = 1$.
    

### Estado final del sistema

- **$R_1$ quedó con $k = \text{"vA"}$**
    
- **$R_2$ quedó con $k = \text{"vB"}$**
    

Ambas réplicas procesaron todos los mensajes y la red quedó en silencio, pero los datos **divergieron de forma permanente**.

Basicamente siempre que haya una lectura y una actualizacion de un valor nunca va haber consisitencia ya que el contador en un evento local como read no se incrementa y en un evento de update no se realiza la comparacion del id de los nodos cuando los tiempos son iguales y en el caso que el otro reloj sea mayor el tiempo no se va a actualizar, ademas el evento de update nunca incrementa el contador

# 4)
## Arquitectura Centralizada (Nodo Primario / Líder por Clave)

En esta topología se utiliza un esquema **Primary-Backup** (o _Single-Leader_) asignado por partición de datos.

### Funcionamiento

- **Asignación de Claves:** Cada clave $k$ tiene un nodo primario $P(k)$ asignado determinísticamente (por ejemplo, mediante una función de hashing $H(k) \bmod n$).
    
- **Escritura (`write`):**
    
    1. Si un cliente envía una escritura a cualquier réplica, esta la redirige al nodo primario $P(k)$.
        
    2. $P(k)$ asigna una marca de tiempo con su reloj escalar local: $C_{primario} = C_{primario} + 1$.
        
    3. $P(k)$ aplica el cambio localmente y transmite un `update(k, v, C_primario)` a todas las réplicas secundarias.
        
    4. Las secundarias aplican la actualización, ajustan su reloj local a $C = \max(C, C_{primario}) + 1$ y responden con un `ACK` al primario.
        
    5. Una vez recibidos todos los `ACK`, $P(k)$ responde al cliente confirmando la escritura.
        
- **Lectura (`read`):**
    
    - Para evitar lecturas obsoletas (_stale reads_), todas las lecturas se redirigen al nodo primario $P(k)$ o requieren una validación de versión con él.

Existe un único punto de ordenamiento ($P(k)$) para cada clave. Al haber una única secuencia de incrementos de reloj para esa clave, es imposible que existan escrituras concurrentes conflictivas o aplicadas en diferente orden entre las réplicas.

## Opción 2: Topología en Anillo con Ficha / Propagación Circular

En este diseño los nodos se organizan en un anillo lógico unidireccional ($P_1 \to P_2 \to \dots \to P_n \to P_1$). Cada nodo $P_i$ es el **dueño primario** de un rango de claves.

### Funcionamiento

- **Escritura (`write`):**
    
    1. La escritura de una clave $k$ debe ser iniciada por el nodo dueño de esa clave, $P_{dueño}$.
        
    2. $P_{dueño}$ incrementa su reloj de Lamport escalar: $C = C + 1$.
        
    3. $P_{dueño}$ aplica el cambio localmente y envía un mensaje `update(k, v, C, id_origen)` a su vecino derecho en el anillo.
        
    4. Cada nodo intermedio al recibir el `update`:
        
        - Ajusta su reloj: $C_{local} = \max(C_{local}, C_{msg}) + 1$.
            
        - Aplica la actualización en su base de datos.
            
        - Reenvía el mensaje al siguiente nodo del anillo.
            
    5. Cuando el mensaje `update` recorre todo el anillo y **regresa al nodo emisor** ($P_{dueño}$), este sabe que todas las réplicas aplicaron la actualización en la misma secuencia lógica. Recién ahí se da por finalizada la operación y se responde al cliente.
        
- **Lectura (`read`):**
    
    - Las lecturas se realizan en el nodo dueño de la clave o se encolan detrás del mensaje de actualización circulante.
    
El anillo actúa como un bus de comunicación de orden FIFO global. Las actualizaciones circulan en una única dirección y cada nodo las procesa exactamente en el orden en que las ve pasar. Ninguna escritura posterior para esa clave puede adelantarse a un mensaje que todavía está circulando por el anillo.

## Opción 3: Arquitectura Totalmente Distribuida (Lamport con ACKs y Cola)

Es la solución simétrica (_Peer-to-Peer_), sin nodos privilegiados ni puntos únicos de falla, basada en el algoritmo de **Difusión con Orden Total de Lamport** (_Total Order Multicast_).

### Funcionamiento

- **Identificador de Evento:** Todo evento se etiqueta con una tupla $req\_id = \langle C_i, \text{ID}_i \rangle$.
    
- **Escritura (`write`):**
    
    1. Cualquier réplica $R_i$ que recibe una escritura hace $C_i = C_i + 1$.
        
    2. Inserta el evento en su `cola_local` ordenada por $\langle C, \text{ID} \rangle$.
        
    3. Envía `update(k, v, req_id)` a todos los demás nodos.
        
- **Recepción y Confirmación:**
    
    1. Cuando un nodo $R_j$ recibe el `update`, actualiza su reloj $C_j = \max(C_j, C_{req}) + 1$, inserta la operación en su `cola_local` en la posición que le corresponde por $\langle C, \text{ID} \rangle$ y envía un `ACK` con su nuevo $C_j$.
        
- **Regla de Commit (Aplicación en memoria):**
    
    - Un nodo solo aplica una actualización cuando esta se encuentra **al frente de su `cola_local`** y ha recibido un `ACK` (o mensaje con marca mayor) de **todos** los demás nodos.
        
- **Lectura (`read`):**
    
    - La lectura se incrementa con $C_i = C_i + 1$, se difunde y se inserta en las colas de todos los nodos para responder el valor exacto cuando le llega su turno de ejecución global.

Gracias a la combinación del desempate por $\text{ID}$ de nodo y la regla de los `ACKs`, **todas las réplicas construyen de forma independiente exactamente la misma cola ordenada de eventos**. Por ende, todas aplican las lecturas y escrituras exactamente en la misma secuencia lineal global.

## Cuadro Comparativo para la Elección

| **Criterio**                  | **Opción 1: Centralizada**  | **Opción 2: Anillo**                    | **Opción 3: Distribuida (Lamport + ACKs)** |
| ----------------------------- | --------------------------- | --------------------------------------- | ------------------------------------------ |
| **Complejidad del algoritmo** | Muy baja                    | Media                                   | Alta                                       |
| **Mensajes por Escritura**    | $O(n)$                      | $O(n)$ (recorrido secuencial)           | $O(n^2)$ (todos a todos)                   |
| **Punto único de falla**      | Sí (el primario)            | Sí (si cae un nodo, el anillo se rompe) | No (totalmente descentralizado)            |
| **Latencia de respuesta**     | Baja (mensajes en paralelo) | Alta (depende del número de saltos $n$) | Alta (espera a todos los ACKs)             |

# 5)
Para resolver estos problemas se suele implementar un algoritmo completo como la **Exclusión Mutua / Difusión con Orden Total de Lamport** (_Total Order Multicast_):

1. **Desempate estricto:** La clave de ordenamiento debe ser la tupla $\langle C_i, \text{ID}_i \rangle$.
    
2. **Relojes de Lamport correctos:** Actualizar $C_i = \max(C_i, C_j) + 1$ al recibir.
    
3. **Petición y Confirmación (_ACKs_):** Todas las réplicas deben guardar las operaciones en una cola ordenada por $\langle C_i, \text{ID}_i \rangle$ y esperar la confirmación (_ACK_) de las demás antes de aplicar el cambio o responder una lectura. De este modo, todas ejecutan exactamente las mismas operaciones y en el mismo orden.

```txt
on msg 'read(key)' from client:
    Ci = Ci + 1
    req_id = <Ci, ID_i>
    agregar a cola_local: <'read', key, req_id, client_id>
    send 'read_request, req_id' a todas las réplicas

on msg 'write(key, value)' from client:
    Ci = Ci + 1
    req_id = <Ci, ID_i>
    agregar a cola_local: <'write', key, value, req_id>
    send 'update(key, value), req_id' a todas las réplicas

on msg 'update(key, value), req_id' from node j:
    Ci = max(Ci, req_id.C) + 1
    agregar a cola_local: <'write', key, value, req_id>
    send 'ack, Ci, ID_i' to node j
```


# 6)
![[ejercicio6p6.excalidraw]]

	