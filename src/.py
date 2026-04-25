class Persona:
    def __init__(self, nombre, cedula):
        self.__nombre = nombre
        self.__cedula = cedula

class Cliente(Persona):
    def __init__(self, nombre, cedula, id_cliente):
        super().__init__(nombre, cedula)
        self.__id_cliente = id_cliente