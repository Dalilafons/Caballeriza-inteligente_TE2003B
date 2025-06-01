import os
import sys
import serial
import time

BAUDRATES = [4800, 9600, 38400, 460800, 57600, 115200, 230400]

class SerialDevice:
    def __init__(self, baudrate: int = 9600):
        self.port = '/dev/serial0'
        if baudrate not in BAUDRATES:
            raise ValueError(f"Baudrate inválido: {baudrate}")

        try:
            self.serial_device = serial.Serial(port=self.port, baudrate=baudrate, timeout=1)
            time.sleep(2)
            self.conectado = True
        except Exception as e:
            print(f"[ERROR] No se pudo abrir el puerto serial: {e}")
            self.serial_device = None
            self.conectado = False

    def send_message(self, message: str) -> str:
        if self.serial_device and self.conectado:
            try:
                self.serial_device.write(message.encode())
                return self.read_message()
            except Exception as e:
                print(f"[ERROR] al enviar mensaje: {e}")
        return "No conectado"

    def read_message(self) -> str:
        if self.serial_device and self.conectado:
            try:
                if self.serial_device.in_waiting > 0:
                    return self.serial_device.readline().decode(errors='ignore').strip()
            except Exception as e:
                print(f"[ERROR] al leer desde el microcontrolador: {e}")
        return ""

    def disconnect(self) -> None:
        if self.serial_device:
            self.serial_device.close()
            print("Conexión serial cerrada.")
            self.conectado = False
