class Cliente:
    def __init__(self, cedula, nombre, id_cliente):
        self.__cedula = cedula
        self.__nombre = nombre
        self.__id_cliente = id_cliente

    def get_cedula(self):
        return self.__cedula

    def get_nombre(self):
        return self.__nombre

    def get_id_cliente(self):
        return self.__id_cliente

    def set_cedula(self, cedula):
        self.__cedula = cedula

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_id_cliente(self, id_cliente):
        self.__id_cliente = id_cliente

    def mostrar(self):
        print("Cédula:", self.__cedula)
        print("Nombre:", self.__nombre)
        print("ID:", self.__id_cliente)

    def __str__(self):
        return self.__nombre + " - " + str(self.__cedula) 