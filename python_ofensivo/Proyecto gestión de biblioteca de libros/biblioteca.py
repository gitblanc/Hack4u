#!/usr/bin/env python3

class Libro:
    def __init__(self, id_libro, autor, nombre_libro, esta_prestado=False):
        self.id_libro = id_libro
        self.autor = autor
        self.nombre_libro = nombre_libro
        self.esta_prestado = esta_prestado


    def __str__(self):
        return f"Libro({self.id_libro}, {self.autor}, {self.nombre_libro})"

    def __repr__(self):
        return self.__str__()


class Biblioteca:
    def __init__(self):
        self.libros = {} # declaramos un diccionario vacío

    def agregar_libro(self, libro):
        if libro.id_libro not in self.libros.keys():
            self.libros[libro.id_libro] = libro
        else:
            print(f"\n[!] no es posible agregar el libro con ID: {libro.id_libro}")

    def prestar_libro(self, id_libro):
        if id_libro in self.libros and not self.libros[id_libro].esta_prestado:
            self.libros[id_libro].esta_prestado = True
        else:
            print(f"\n[!] No es posible prestar el libro con ID: {id_libro}")

    @property
    def mostrar_libros(self):
        return [libro for libro in self.libros.values() if not libro.esta_prestado]

    @property
    def mostrar_libros_prestados(self):
        return [libro for libro in self.libros.values() if libro.esta_prestado]

class BibliotecaInfantil(Biblioteca):
    def __init__(self):
        super().__init__() # se llama al constructor original
        self.libros_para_kids = {}

    def agregar_libro(self, libro, es_para_kids):
        super().agregar_libro(libro)
        self.libros_para_kids[libro.id_libro] = es_para_kids

    def prestar_libro(self, id_libro, es_para_kids):
        if id_libro in self.libros and self.libros_para_kids[id_libro] == es_para_kids and not self.libros[id_libro].esta_prestado:
            self.libros[id_libro].esta_prestado = True
        else:
            print(f"\n[!] No es posible prestar el libro con ID: {id_libro}")
    
    @property
    def mostrar_libros_para_kids(self):
        return self.libros_para_kids


if __name__ == '__main__':
    biblioteca = BibliotecaInfantil()

    libro1 = Libro(1, "Marcelo Vázquez", "¿Cómo ser un Lammer de Potencia máxima?")
    libro2 = Libro(2, "Pepito Manolete", "Aprende a colorear desde 0")

    # print(libro1)
    # print(libro2)

    biblioteca.agregar_libro(libro1, es_para_kids = False)
    biblioteca.agregar_libro(libro2, es_para_kids = True)

    print(f"\n[+] Libros en la biblioteca: {biblioteca.mostrar_libros}") # Para evitar que salga <<object xxxx>>, hay que definir el método especial __repr__

    biblioteca.prestar_libro(1, es_para_kids = False)

    print(f"\n[+] Libros en la biblioteca: {biblioteca.mostrar_libros}")
    print(f"\n[+] Libros prestados: {biblioteca.mostrar_libros_prestados}")
    print(f"\n[+] Libros para niños: {biblioteca.mostrar_libros_para_kids}")