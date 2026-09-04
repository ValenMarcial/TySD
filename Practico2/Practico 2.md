## 1) 
```python
CODEWORDS = [
  "000",
  "001",
  "010",
  "011",
  "101",
  "100",
  "110",
  "111"
]
```
para este codewords la paridad par da como resultado:
```bash
{'000': '0000', '001': '0011', '010': '0101', '011': '0110', '101': '1010', '100': '1001', '110': '1100', '111': '1111'}
```
y nos da una distancia de hamming de 2.
Con esto vemos que:
detectar: 2 >= d + 1 donde d como maximo es 1
corregir: 2 >= 2*d + 1 donde d como maximo es 0

Realizar este despeje te entrega directamente el número máximo de errores simultáneos que el esquema de codificación es capaz de tolerar.

## 2)
4 bits de datos
Cada palabra se arregla en forma de matrix 2x2 
Se agrega un bit de paridad por cada fila y por cada columna obteniendo un codigo de 3x3 bits

11 0
01 1
10 1

cada vez que cambie un bit en la zona 11, 01 produce que el bit de paridad tenga que cambiar en la fila y en la columna.
pero eso mismo hace que la columna de la paridad tambien tenga que cambiar por lo tanto para corregir tuvimos que hacer 4 cambios para tener una codeword valida, por lo tanto la distancia hamming es de 4.

detectar es 4 = d + 1 entonces d = 3 se pueden detectar hasta 3 errores 
corregir es 4 = 2d+1 entonces d = 1 se puede corregir solo 1 error

## 4)
### a) y b)
mensaje = 11010011 

usando G(x) = x^3 + x^2 + 1 ahora deberiamos tradicir a la representacion binaria osea (1 * x^3) + (1*x^2) + (0*x^1) + (1 *x^0) osea 1101

como el grado del polinomio es 3 agregaremos 3 bits al mensaje
mensaje' = 11010011000

Ahora hay que dividir modulo 2, que es aplicar el XOR de izquierda a derecha
```txt
1101  11010011000 como el bloque empieza con 1 entonces el cociente empieza con 1
      -----------
      0000        los primeros 4 bits son 0

      00000011000
ahora avanzamos hacia la derecha buscando el proximo 1
en este procedimiento bajamos dos 0 y cuando bajo el 1 todavia no completamos 4 bits por lo que agrego cinco 0s
hasta llegar a tener un bloque con 4 bits que empiece con 1. por eso el cociente es 1000001
      00000011000
            1101  se formo el bloque 1100
aplicamos XOR
      1100
      1101
      ----
      0001
bajando el ultimo bit que quedo y el bloque nuevo empieza con 0 osea al cociente se le agrega un 0 y queda 10000010
        010
como solo tiene 3 bits y es mas pequeño que nuestro divisor no entra por lo que termina la division el resto es 010
```
Entonces el `CRC` es 010

El receptor usa el mismo algoritmo que el emisor divide lo que le llego por el polinomio generador, evalua si el resto es 000 el mensaje es valido e integro, si no se descarta el paquete por que sufrio corrupcion en el medio fisico.

El ejercicio b es basicamente concatenar el CRC al mensaje nada mas.

### c ) Casos de Recepcion
Para la simulacion el emisor reemplaza los 3 ceros anexados por el valor del CRC
#### Caso A: Recepcion sin errores
El receptor recive exactamente lo enviado
11010011010 paquete que recibimos

Comenzamos a dividir por el generador 1101
```txt
11010011010
1101
===========
00000011010
      1101
      ====
      00000 bajamos el cero restante
```
El resto es 0 el paquete fue aceptado

#### Caso B: Recepcion con errores
11010010010 paquete recibido corrupto

Comenzamos a dividir por el generador 1101
```txt
11010010010
1101
===========
00000010010
      1101
      ====
      01000
       1101
       ====
       0101
```
El resto es 0101 por lo tanto el paquete esta corrupto y se descarta


## 5)

![[Ejercicio5P2.excalidraw]]

### e)
![[Eje5P2e.excalidraw]]

## 6)
Leer [[Practico2/README|README]] para ejecutar kathara con la configuracion que creamos
Para agregar una nueva pc al mismo switch se agrega al lab.conf esto
pc3[0]="A/00:00:00:00:00:03"
pc3[image]="kathara/base"
pc3[ipv6]="false"
