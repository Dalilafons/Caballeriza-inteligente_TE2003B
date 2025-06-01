import tkinter as tk
import serial
import time

try:
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
    time.sleep(2)
except:
    ser = None

datos = {
    "TEMP": "--",
    "HUMO": "NO",
    "DOOR": "UNKNOWN",
    "AGUA": "OFF",
    "ALIM": "OFF"
}

# === GUI ===
root = tk.Tk()
root.title("🐴 Caballeriza Inteligente")
root.geometry("400x450")
root.configure(bg="#F4F0E6")

font_title = ("Arial", 16, "bold")
font_normal = ("Arial", 12)

label_conexion = tk.Label(root, text="Desconectado ❌", font=font_title, bg="#F4F0E6", fg="red")
label_conexion.pack(pady=10)

label_temp = tk.Label(root, text="🌡️ Temperatura: --", font=font_normal, bg="#F4F0E6")
label_temp.pack()

label_humo = tk.Label(root, text="🔥 Humo: --", font=font_normal, bg="#F4F0E6")
label_humo.pack()

label_puerta = tk.Label(root, text="🚪 Puerta: --", font=font_normal, bg="#F4F0E6")
label_puerta.pack()

label_agua = tk.Label(root, text="💧 Agua: --", font=font_normal, bg="#F4F0E6")
label_agua.pack()

label_alimento = tk.Label(root, text="🍽️ Alimento: --", font=font_normal, bg="#F4F0E6")
label_alimento.pack()

# === Funciones ===
def enviar_comando(comando):
    if ser:
        ser.write((comando + "\n").encode())

def actualizar_datos():
    if ser and ser.in_waiting > 0:
        linea = ser.readline().decode('utf-8').strip()
        partes = linea.split(",")
        for p in partes:
            if ":" in p:
                k, v = p.split(":")
                if k in datos:
                    datos[k] = v

    label_conexion.config(text="Conectado ✅" if ser else "Desconectado ❌", fg="green" if ser else "red")
    label_temp.config(text=f"🌡️ Temperatura: {datos['TEMP']}°C")
    label_humo.config(text=f"🔥 Humo: {datos['HUMO']}")
    label_puerta.config(text=f"🚪 Puerta: {datos['DOOR']}")
    label_agua.config(text=f"💧 Agua: {datos['AGUA']}")
    label_alimento.config(text=f"🍽️ Alimento: {datos['ALIM']}")

    root.after(1000, actualizar_datos)

# === Botones ===
tk.Button(root, text="Abrir Puerta 🚪", font=font_normal, bg="#A3E4D7", command=lambda: enviar_comando("CMD:DOOR:OPEN")).pack(pady=5, fill="x")
tk.Button(root, text="Cerrar Puerta 🚪", font=font_normal, bg="#E6B0AA", command=lambda: enviar_comando("CMD:DOOR:CLOSE")).pack(pady=5, fill="x")

tk.Button(root, text="Activar Agua 💧", font=font_normal, bg="#D1F2EB", command=lambda: enviar_comando("CMD:AGUA:ON")).pack(pady=5, fill="x")
tk.Button(root, text="Detener Agua 💧", font=font_normal, bg="#FADBD8", command=lambda: enviar_comando("CMD:AGUA:OFF")).pack(pady=5, fill="x")

tk.Button(root, text="Dar Alimento 🍽️", font=font_normal, bg="#D7BDE2", command=lambda: enviar_comando("CMD:ALIM:ON")).pack(pady=5, fill="x")

# === Iniciar ===
actualizar_datos()
root.mainloop()
