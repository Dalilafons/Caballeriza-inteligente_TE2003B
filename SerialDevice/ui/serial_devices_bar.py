from tkinter import Button, Frame, Text, END
from tkinter.ttk import Label, Style
from SerialDevice.serial_device import SerialDevice

class SerialDeviceBar(Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.micro = SerialDevice()
        self.config = master.config if hasattr(master, 'config') else {}

        ui = self.config.get('ui', {})
        font_cfg = (ui.get('font_family', 'Arial'), ui.get('font_size', 14))
        font_color = ui.get('font_color', '#000000')

        buttons_cfg = ui.get('buttons', {})
        send_cfg = buttons_cfg.get('send', {})
        disconnect_cfg = buttons_cfg.get('disconnect', {})
        close_cfg = buttons_cfg.get('close', {})

        textboxes_cfg = ui.get('textboxes', {})
        input_cfg = textboxes_cfg.get('input', {})
        output_cfg = textboxes_cfg.get('output', {})

        # === Estilos ===
        style = Style()
        style.configure("TLabel", foreground=font_color, font=font_cfg)

        # === Etiquetas principales ===
        self.label_status = Label(self, text='Estado de conexión: Desconectado ❌', style="TLabel")
        self.label_status.pack(padx=5, pady=5, fill='x')

        self.label_temp = Label(self, text='🌡️ Temperatura: --', style="TLabel")
        self.label_temp.pack(padx=5, pady=5, fill='x')

        self.label_humo = Label(self, text='🔥 Humo: --', style="TLabel")
        self.label_humo.pack(padx=5, pady=5, fill='x')

        self.label_puerta = Label(self, text='🚪 Puerta: --', style="TLabel")
        self.label_puerta.pack(padx=5, pady=5, fill='x')

        self.label_agua = Label(self, text='💧 Agua: --', style="TLabel")
        self.label_agua.pack(padx=5, pady=5, fill='x')

        self.label_alimento = Label(self, text='🍽️ Alimento: --', style="TLabel")
        self.label_alimento.pack(padx=5, pady=5, fill='x')

        # === Botones ===
        self.btn_abrir_puerta = Button(self, text="Abrir Puerta 🚪", font=font_cfg, bg="#A3E4D7", command=lambda: self.enviar_comando("CMD:DOOR:OPEN"))
        self.btn_abrir_puerta.pack(pady=2, fill='x')

        self.btn_cerrar_puerta = Button(self, text="Cerrar Puerta 🚪", font=font_cfg, bg="#E6B0AA", command=lambda: self.enviar_comando("CMD:DOOR:CLOSE"))
        self.btn_cerrar_puerta.pack(pady=2, fill='x')

        self.btn_activar_agua = Button(self, text="Activar Agua 💧", font=font_cfg, bg="#D1F2EB", command=lambda: self.enviar_comando("CMD:AGUA:ON"))
        self.btn_activar_agua.pack(pady=2, fill='x')

        self.btn_detener_agua = Button(self, text="Detener Agua 💧", font=font_cfg, bg="#FADBD8", command=lambda: self.enviar_comando("CMD:AGUA:OFF"))
        self.btn_detener_agua.pack(pady=2, fill='x')

        self.btn_dar_alimento = Button(self, text="Dar Alimento 🍽️", font=font_cfg, bg="#D7BDE2", command=lambda: self.enviar_comando("CMD:ALIM:ON"))
        self.btn_dar_alimento.pack(pady=2, fill='x')

        self.after(1000, self.actualizar_datos)

    def enviar_comando(self, comando):
        if self.micro and self.micro.conectado:
            self.micro.send_message(comando + "\n")

    def actualizar_datos(self):
        if self.micro and self.micro.conectado:
            respuesta = self.micro.read_message()
            if respuesta:
                try:
                    datos = dict(item.split(":") for item in respuesta.split(",") if ":" in item)
                    self.label_temp.config(text=f"🌡️ Temperatura: {datos.get('TEMP', '--')}°C")
                    self.label_humo.config(text=f"🔥 Humo: {datos.get('HUMO', '--')}")
                    self.label_puerta.config(text=f"🚪 Puerta: {datos.get('DOOR', '--')}")
                    self.label_agua.config(text=f"💧 Agua: {datos.get('AGUA', '--')}")
                    self.label_alimento.config(text=f"🍽️ Alimento: {datos.get('ALIM', '--')}")
                    self.label_status.config(text="Estado de conexión: Conectado ✅")
                except Exception as e:
                    print(f"Error al procesar datos: {e}")
        else:
            self.label_status.config(text="Estado de conexión: Desconectado ❌")

        self.after(1000, self.actualizar_datos)
