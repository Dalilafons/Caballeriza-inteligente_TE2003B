from tkinter import Button
from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter.ttk import Label
from tkinter import Text
from tkinter import END

from SerialDevice.serial_device import SerialDevice
from SerialDevice.serial_device import BAUDRATES

from tkinter.ttk import Style


class SerialDeviceBar(Frame):
    def __init__(self, master = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.arduino = None
        self.config = master.config if hasattr(master, 'config') else {}  # obtiene config del MainApp

        #AQUI VA TU BLOQUE
        ui = self.config.get('ui', {})
        font_cfg  = (ui.get('font_family', 'Arial'), ui.get('font_size', 14))
        font_color = ui.get('font_color', '#000000')

        # Configuración de colores desde YAML
        buttons_cfg = self.config.get('ui', {}).get('buttons', {})

        send_cfg = buttons_cfg.get('send', {})
        disconnect_cfg = buttons_cfg.get('disconnect', {})
        close_cfg = buttons_cfg.get('close', {})

        textboxes_cfg = ui.get('textboxes', {})
        input_cfg = textboxes_cfg.get('input', {})
        output_cfg = textboxes_cfg.get('output', {})

        # === Estilo para Combobox ===
        style = Style()
        style.configure("CustomCombobox.TCombobox",
                        foreground=font_color,
                        background='white',
                        fieldbackground='white',
                        selectforeground=font_color,
                        selectbackground='#E0E0E0')
        
        # === Widgets ===
        self.serial_devices_label = Label(self, text='Pick a serial port:', font=font_cfg, foreground=font_color)

        self.serial_devices_label = Label(
            self,
            text='Pick a serial port:',
            font=font_cfg,
            foreground=font_color
        )

        self.serial_devices_combobox = Combobox(
            self,
            values = self.get_available_serial_ports(),
            font=font_cfg,
            style="CustomCombobox.TCombobox"
        )

        self.baudrates_combobox = Combobox(
            self,
            values=BAUDRATES,
            font=font_cfg,
            style="CustomCombobox.TCombobox"
        )

        self.send_message_label = Label(
            self,
            text = 'Send a message to Arduino → ',
            font=font_cfg,
            foreground=font_color
        )

        self.textbox = Text(
            self,
            font=font_cfg,
            foreground=input_cfg.get('text_color', '#000000'),
            background=input_cfg.get('bg_color', "#D4D3D3"),
            height = 2
        )

        self.send_message_button = Button(
            self,
            text='Send Message',
            font=font_cfg,
            foreground=send_cfg.get('text_color', '#FFFFFF'),
            background=send_cfg.get('bg_color', "#31CAE8"),
            command=self.send_message
        )

        self.read_message_label = Label(
            self,
            text = 'Received a message from Arduino → Caesar Cipher',
            font=font_cfg, 
            foreground=font_color
        )

        self.textbox_received_message = Text(
            self,
            font=font_cfg,
            foreground=output_cfg.get('text_color', '#000000'),
            background=output_cfg.get('bg_color', '#FFFFFF'),
            height = 2
        )
        self.init_gui()

        self.disconnect_button = Button(
            self,
            text='Disconnect Arduino',
            font=font_cfg,
            foreground=disconnect_cfg.get('text_color', '#FFFFFF'),
            background=disconnect_cfg.get('bg_color', "#EF251A"),
            command=self.disconnect_arduino
        )
        self.disconnect_button.pack(side='top', padx=5, pady=5, fill='x')

        self.close_button = Button(
            self,
            text='Close App',
            font=font_cfg,
            foreground=close_cfg.get('text_color', '#FFFFFF'),
            background=close_cfg.get('bg_color', '#111111'),
            command=master.on_close  # llama al método de cierre de MainApp
        )
        self.close_button.pack(side='top', padx=5, pady=5, fill='x')

    def init_gui(self):
        self.serial_devices_combobox.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.serial_devices_label.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.baudrates_combobox.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.serial_devices_combobox.current(0)
        self.baudrates_combobox.current(0)

        self.serial_devices_combobox.bind('<<ComboboxSelected>>', lambda x: self.connect_arduino())
        
        self.send_message_label.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.textbox.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.send_message_button.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.read_message_label.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.textbox_received_message.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        
    
    def get_available_serial_ports(self)->list[str]:
        port_list = ['Port:']
        port_list.extend(SerialDevice.find_available_serial_ports())
        return port_list

    def connect_arduino(self):
        if self.arduino is None and self.serial_devices_combobox.get() != 'Port:':
            self.arduino = SerialDevice(
                port=self.serial_devices_combobox.get(),
                baudrate=int(self.baudrates_combobox.get())
            )
        elif self.serial_devices_combobox.get() != 'Port:':
            self.arduino.disconnect()
            self.arduino = SerialDevice(
                port=self.serial_devices_combobox.get(),
                baudrate=int(self.baudrates_combobox.get())
            )
    
    #def send_message(self,):
    #    print("Botón presionado, enviando mensaje al Arduino...")
    #    text_to_send = self.textbox.get("1.0", END) +'\n'
    #    if self.arduino is not None:
    #        received=self.arduino.send_message(text_to_send)
    #        self.textbox_received_message.insert("1.0", received)
    
    def send_message(self):
        print("Botón presionado, enviando mensaje al Arduino...")

        # 1. Obtener el texto del campo ANTES de borrar
        text_to_send = self.textbox.get("1.0", END).strip()

        # 2. Verificar que no esté vacío
        if not text_to_send:
            print("No se puede enviar un mensaje vacío.")
            return

        # 3. Enviar solo si Arduino está conectado
        if self.arduino is not None:
            # No borrar aún
            print(f"Texto a enviar: {text_to_send}")
            response = self.arduino.send_message(text_to_send)

            # 4. Mostrar la respuesta
            self.textbox_received_message.config(state='normal')
            self.textbox_received_message.delete("1.0", END)
            self.textbox_received_message.insert(END, response)
            self.textbox_received_message.config(state='disabled')

            # 5. AHORA sí borrar el contenido del campo de entrada
            #self.textbox.delete("1.0", END)

    def disconnect_arduino(self):
        if self.arduino is not None:
            self.arduino.disconnect()
            self.arduino = None
            print("Arduino desconectado manualmente.")


