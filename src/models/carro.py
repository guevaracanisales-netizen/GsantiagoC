class Carro:
    def __init__(self, placa, modelo, anio, marca):
        self.__placa  = placa
        self.__modelo = modelo
        self.__anio   = anio
        self.__marca  = marca

    def get_placa(self):
        return self.__placa

    def get_modelo(self):
        return self.__modelo

    def get_anio(self):
        return self.__anio

    def get_marca(self):
        return self.__marca

    def set_placa(self, placa):
        self.__placa = placa

    def set_modelo(self, modelo):
        self.__modelo = modelo

    def set_anio(self, anio):
        self.__anio = anio

    def set_marca(self, marca):
        self.__marca = marca

    def mostrar(self):
        print("Placa:",  self.__placa)
        print("Modelo:", self.__modelo)
        print("Año:",    self.__anio)
        print("Marca:",  self.__marca)

    def __str__(self):
        return f"{self.__placa} - {self.__marca} {self.__modelo} ({self.__anio})"