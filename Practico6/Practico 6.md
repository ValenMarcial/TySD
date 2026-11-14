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
