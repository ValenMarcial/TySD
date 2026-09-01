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

## 3)
