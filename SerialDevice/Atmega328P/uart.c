// Caballeriza Inteligente - ATmega328P
// Baudrate 9600, F_CPU 8MHz

#include <mega328p.h>
#include <delay.h>
#include <stdio.h>
#include <string.h>

#define DOOR_PORT PORTB.0
#define AGUA_PORT PORTB.1
#define ALIM_PORT PORTB.2

char comando[30];
unsigned char idx = 0;

// Estados simulados
char door_state[10] = "CLOSED";
char agua_state[4] = "OFF";
char alim_state[4] = "OFF";
char humo_state[4] = "NO";
int temp = 26;

// Prototipos
void enviar_datos();
void procesar_comando();

interrupt [USART_RXC] void uart_rx_isr(void) {
    char c = getchar();
    if (c == '\n') {
        comando[idx] = '\0';
        procesar_comando();
        idx = 0;
    } else if (idx < sizeof(comando) - 1) {
        comando[idx++] = c;
    }
}

void procesar_comando() {
    if (strcmp(comando, "CMD:DOOR:OPEN") == 0) {
        DOOR_PORT = 1;
        strcpy(door_state, "OPEN");
    } else if (strcmp(comando, "CMD:DOOR:CLOSE") == 0) {
        DOOR_PORT = 0;
        strcpy(door_state, "CLOSED");
    } else if (strcmp(comando, "CMD:AGUA:ON") == 0) {
        AGUA_PORT = 1;
        strcpy(agua_state, "ON");
    } else if (strcmp(comando, "CMD:AGUA:OFF") == 0) {
        AGUA_PORT = 0;
        strcpy(agua_state, "OFF");
    } else if (strcmp(comando, "CMD:ALIM:ON") == 0) {
        ALIM_PORT = 1;
        strcpy(alim_state, "ON");
        delay_ms(1000); // Simula dispensador
        ALIM_PORT = 0;
        strcpy(alim_state, "OFF");
    }
}

void enviar_datos() {
    printf("TEMP:%d,HUMO:%s,DOOR:%s,AGUA:%s,ALIM:%s\n", temp, humo_state, door_state, agua_state, alim_state);
}

void main() {
    // Configuración de USART0
    UCSRB = (1 << RXEN) | (1 << TXEN) | (1 << RXCIE); // Rx, Tx y Rx Interrupt
    UBRRL = 51; // Para 9600 baud con 8MHz

    // Configuración de salidas
    DDRB.0 = 1; // DOOR
    DDRB.1 = 1; // AGUA
    DDRB.2 = 1; // ALIM

    #asm("sei") // Habilita interrupciones

    while (1) {
        enviar_datos();
        delay_ms(1000);
    }
}

