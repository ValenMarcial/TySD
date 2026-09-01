#include <stdio.h>
#include <stdint.h>

uint16_t cksum(uint16_t *buf, int count);

uint16_t cksum(uint16_t *buf, int count)
{
    register uint32_t sum = 0;

    while (count--)
    {
        sum += *buf++;
        if (sum & 0xFFFF0000)
        {
            /* carry occurred, so wrap around */
            sum &= 0xFFFF;
            sum++;
        }
    }
    return ~(sum & 0xFFFF);
}

int main() {
    int data_length = 4;
    int packet_length = 5;
    uint16_t packet[5];

    // Datos simulados
    packet[0] = 0x4500;
    packet[1] = 0x0030;
    packet[2] = 0x4422;
    packet[3] = 0x4000;

    packet[4] = cksum(packet, data_length);
    printf("Checksum calculado y en el paquete \n");

    printf("Recepcion transmision exitosa \n");
    uint16_t verificacion_exitosa = cksum(packet, packet_length);

    if (verificacion_exitosa == 0x0000)
    {
        printf("Resultado 0x0000 \n");
        printf("Estado del paquete aceptado. Datos integros. \n \n");
    } 
    else 
    {
        printf("Paquete rechazado \n");
    }

    printf("Recepcion datos corruptos \n");
    uint16_t corrupted_packet[5];

    for (int i = 0; i < packet_length; i++) {
        corrupted_packet[i] = packet[i];
    }

    corrupted_packet[1] = 0x0031;
    
    uint16_t verificacion_fallida = cksum(corrupted_packet, packet_length);
    
    if (verificacion_fallida == 0x0000)
    {
        printf("Estado paquete aceptado erroneamente \n");
    }
    else
    {
        printf("Resultado del calculo: 0x%04X\n", verificacion_fallida);
        printf("Error detectado, resultado != 0x0000 paquete descartado\n");
    }

    return 0;
}