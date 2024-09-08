#!/usr/bin/env python3

class Animal:
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie
        self.alimentado = False
    
    def __str__(self):
        return f"[{self.especie.upper()}] {self.nombre} - {'Alimentado' if self.alimentado else 'Hambriento'}"
    
    def alimentar(self):
        self.alimentado = True
    
    def vender(self):
        self.alimentado = False

class TiendaAnimales:
    def __init__(self, nombre):
        self.nombre = nombre
        self.animales = [] # lista

    def agregar_animal(self, animal):
        self.animales.append(animal)

    def mostrar_animales(self):
        for animal in self.animales:
            print(animal)

    def alimentar_animales(self):
        for animal in self.animales:
            animal.alimentar()

    def vender_animal(self, nombre):
        for animal in self.animales:
            if animal.nombre == nombre:
                animal.vender()
                self.animales.remove(animal)
                
        print(f"[!] No se ha encontrado ningún animal en la tienda con nombre {nombre}")

if __name__ == '__main__':
    tienda = TiendaAnimales("Mi Tienda de Animales")

    gato = Animal("Tijuana", "Gato")
    perro = Animal("Cachopo", "Perro")

    tienda.agregar_animal(gato)
    tienda.agregar_animal(perro)

    tienda.mostrar_animales()
    
    tienda.alimentar_animales()

    tienda.mostrar_animales()

    tienda.vender_animal("Tijuana")

    tienda.mostrar_animales()