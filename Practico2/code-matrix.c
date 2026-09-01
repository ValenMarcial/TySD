#include <stdio.h>
#include <stdint.h>

void calculate_parity(uint8_t mensaje);
void print_matrix(int matrix[3][3]);
void corregir_error(int matrix[3][3]);

void calculate_parity(uint8_t mensaje) {
    int matrix [3][3];

    matrix[0][0] = (mensaje >> 3) & 1;
    matrix[0][1] = (mensaje >> 2) & 1;
    matrix[1][0] = (mensaje >> 1) & 1;
    matrix[1][1] = (mensaje >> 0) & 1;

    matrix[0][2] = matrix[0][0] ^ matrix[0][1];
    matrix[1][2] = matrix[1][0] ^ matrix[1][1];

    matrix[2][0] = matrix[0][0] ^ matrix[1][0];
    matrix[2][1] = matrix[0][1] ^ matrix[1][1];

    matrix[2][2] = matrix[2][0] ^ matrix[2][1];

    print_matrix(matrix);
}

void print_matrix(int matrix[3][3]) {
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            printf("%d", matrix[i][j]);
        }
        printf("\n");
    }
}

void corregir_error(int matrix[3][3]) {
    int error_fila = -1;
    int error_col = -1;

    for (int i = 0; i < 2; i++) {
        if ((matrix[i][0] ^ matrix[i][1]) != matrix[i][2]) {
            error_fila = i;
        }
    }

    for (int j = 0; j < 2; j++) {
        if ((matrix[0][j] ^ matrix[1][j]) != matrix[2][j]) {
            error_col = j;
        }
    }

    if (error_fila != -1 && error_col != -1) {
        matrix[error_fila][error_col] ^= 1; 
        printf("Corregido: Bit de datos en [%d][%d]\n", error_fila, error_col);
        
    } else if (error_fila != -1 && error_col == -1) {
        // Sin cruce: Error exclusivo en el bit de paridad de esa fila
        matrix[error_fila][2] ^= 1;
        printf("Corregido: Paridad de fila en [%d][2]\n", error_fila);
        
    } else if (error_fila == -1 && error_col != -1) {
        matrix[2][error_col] ^= 1;
        printf("Corregido: Paridad de columna en [2][%d]\n", error_col);
        
    } else {
        if ((matrix[0][2] ^ matrix[1][2]) != matrix[2][2]) {
            matrix[2][2] ^= 1;
            printf("Corregido: Paridad cruzada en [2][2]\n");
        } else {
            printf("Válido: No se detectaron errores simples.\n");
        }
    }
}

int main() {
    uint8_t mensaje = 0b1101;

    printf("Datos (word)= %d%d%d%d\n", 
           (mensaje >> 3) & 1, (mensaje >> 2) & 1, 
           (mensaje >> 1) & 1, mensaje & 1);
    
    calculate_parity(mensaje);

    int codeword_recibido[3][3] = {
        {1, 1, 1}, 
        {1, 1, 0}, 
        {0, 1, 1}
    };

    corregir_error(codeword_recibido);
    return 0;
}
