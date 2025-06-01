import os
import sys
import serial
import time

BAUDRATES = [4800, 9600, 38400, 460800, 57600, 115200, 230400]

class SerialDevice:
    def __init__(self, port: str, baudrate: int):
        if baudrate not in BAUDRATES:
            raise ValueError(f"Invalid baudrate: {baudrate}")
        if port not in self.find_available_serial_ports():
            raise ValueError(f"Invalid port: {port}")
        self.serial_device = serial.Serial(port=port, baudrate=baudrate)
        time.sleep(2)
        self.serial_device.write(b"Connect")

    def send_message(self, message: str) -> str:
        print(f"Enviando al Arduino: {message.strip()}")
        self.serial_device.write(message.encode())
        time.sleep(1)
        return self.read_message()

    def read_message(self) -> str:
        try:
            if self.serial_device.in_waiting > 0:
                return self.serial_device.readline().decode(errors='ignore').strip()
            return "Sin datos recibidos"
        except Exception as e:
            print(f"[ERROR] al leer desde el Arduino: {e}")
            return "Error al leer"

    def receive_message(self) -> str:
        return self.serial_device.readline().decode()

    def disconnect(self) -> None:
        self.serial_device.close()
        print("Serial connection closed.")

    @staticmethod
    def find_available_serial_ports() -> list[str]:
        if sys.platform.startswith('darwin'):
            ports = os.listdir('/dev/')
            ports = [f"/dev/{port}" for port in ports if port.startswith('cu.')]
        elif sys.platform.startswith('linux'):
            ports = os.listdir('/dev/')
            ports = [f"/dev/{port}" for port in ports if port.startswith('ttyA') or port.startswith('ttyUSB') or port.startswith('ttyAMA')]
        elif sys.platform.startswith('win'):
            ports = [f'COM{n}' for n in range(1, 256)]
        else:
            return []
        return ports
