#!/usr/bin/env python3

import tkinter as tk

class Calculadora:
    def __init__(self, master):
        self.master = master
        self.display = tk.Entry(master, width=15, font=("Arial", 23), bd=10, insertwidth=1, bg="#6495de", justify="right")
        self.display.grid(row=0, column=0, columnspan=4)
        self.op_verification = False
        self.current = ''
        self.op = ''
        self.total = 0

        row = 1 # es 1 porque el display es 0
        col = 0

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", ".", "+",
            "="
        ]

        for button in buttons:
            self.build_button(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.master.bind("<Key>", self.key_press) # manejador de eventos especial (para registrar los caracteres por teclado)

    def key_press(self, event):
        key = event.char

        if key == "\r":
            self.calculate()
            return # para que los caracteres especiales no se envíen a click()
        elif key == "\x08":
            self.clear_display()
            return()
        elif key == "\x1b":
            self.master.quit()
            return

        self.click(key)

    def clear_display(self):
        self.display.delete(0, tk.END)
        self.op_verification = False
        self.current = ''
        self.op = ''
        self.total = 0

    def calculate(self):
        if self.current and self.op:
            if self.op == "/":
                self.total /= float(self.current)
            elif self.op == "*":
                self.total *= float(self.current)
            elif self.op == "+":
                self.total += float(self.current)
            elif self.op == "-":
                self.total -= float(self.current)
        
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, round(self.total,3))

    def click(self, key):
        if self.op_verification:
            self.op_verification = False

        self.display.insert(tk.END, key) # también se puede poner "end"

        if key in "0123456789" or key == ".":
            self.current += key
        else:
            if self.current:
                if not self.op:
                    self.total = float(self.current)

            self.current = ''
            self.op_verification = True
            self.op = key

    def build_button(self, button, row, col):      
        if button == "C":  
            #b = tk.Button(self.master, text=button, width=3, command=self.clear_display) # si pones los paréntesis en la función, ésta se llama al crear el botón
            b = tk.Button(self.master, text=button, width=3, command=lambda: self.clear_display()) # para ello usar funciones lambda
        elif button == "=":
            b = tk.Button(self.master, text=button, width=3, command=lambda: self.calculate())
        else:
            b = tk.Button(self.master, text=button, width=3, command=lambda: self.click(button))
        b.grid(row=row, column=col)



root = tk.Tk()

my_gui = Calculadora(root)

root.mainloop()