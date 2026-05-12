from abc import ABC, abstractmethod

class Pasajero(ABC):          # ← clase abstracta (abstracción)
    def __init__(self, cedula, nombre):
        self.__cedula = cedula
        self.__nombre = nombre

    def get_cedula(self):
        return self.__cedula

    def get_nombre(self):
        return self.__nombre

    def set_cedula(self, cedula):
        self.__cedula = cedula

    def set_nombre(self, nombre):
        self.__nombre = nombre

    @abstractmethod          # ← método abstracto obligatorio
    def mostrar(self):       # cada subclase DEBE implementarlo
        pass

    def __str__(self):
        return f"{self.__nombre} - {self.__cedula}"