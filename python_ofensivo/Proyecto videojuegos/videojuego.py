#!/usr/bin/env python3

juegos = ["Super Mario Bros", "Zelda Breath of the Wild", "Cyberpunk", "Final Fantasy 7"]
tope = 100

# Géneros

generos = {
    "Super Mario Bros": "Aventura",
    "Zelda Breath of the Wild": "Aventura",
    "Cyberpunk": "Rol",
    "Final Fantasy 7": "Rol"
}

# Ventas y Stock
ventas_y_stock = {
    "Super Mario Bros": (400,200),
    "Zelda Breath of the Wild": (600,20),
    "Cyberpunk": (60,120),
    "Final Fantasy 7": (924,3)
}

# Clientes
clientes = {
    "Super Mario Bros": {"Marcelo", "Hackermate", "Hackavis", "Securiters","Lobotec"},
    "Zelda Breath of the Wild": {"Marcelo", "Hackermate", "Hackavis", "Lucía", "Manolo", "Pepe"},
    "Cyberpunk": {"Hackermate", "Lobotec", "Pepe", "Raquel", "Albert"},
    "Final Fantasy 7": {"Lucía", "Manolo", "Pepe", "Securiters", "Patricia", "Raquel"}
}

mi_juego = "Super Mario Bros"

# Sumario
def sumario(juego):
    print(f"\n[i] Resumen del juego {juego}")
    print(f"\n\t[+] Género del juego: {generos[juego]}")
    print(f"\n\t[+] Total de ventas del juego: {ventas_y_stock[juego][0]} unidades")
    print(f"\n\t[+] Total de stock del juego: {ventas_y_stock[juego][1]} unidades")
    print(f"\n\t[+] Clientes que han adquirido el juego: {', '.join(clientes[juego])}") # para separar los clientes por , en lugar de ver un diccionario

for juego in juegos:
    if ventas_y_stock[juego][0] > tope: 
        sumario(juego)

ventas_totales = lambda: sum(ventas for ventas, _ in ventas_y_stock.values()) # el _ es para indicar que no me interesa el 2 elemento
print(f"El total de ventas de todos los productos ha sido de {ventas_totales()} productos") # acordarse de llamar a la función con los ()

ventas_totales2 = lambda: sum(ventas for juego, (ventas, _) in ventas_y_stock.items() if ventas_y_stock[juego][0] > tope) 
print(f"El total de ventas de todos los productos con más de {tope} ventas de tope ha sido de {ventas_totales2()} productos")

