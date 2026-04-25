class Reserva:
    def __init__(self, cliente, hora_salida, hora_llegada, sector):
        self.__cliente = cliente
        self.__hora_salida = hora_salida
        self.__hora_llegada = hora_llegada
        self.__sector = sector
        self.__confirmado = False

    def get_cliente(self):
        return self.__cliente

    def get_hora_salida(self):
        return self.__hora_salida

    def get_hora_llegada(self):
        return self.__hora_llegada

    def get_sector(self):
        return self.__sector

    def get_confirmado(self):
        return self.__confirmado

    def set_hora_salida(self, hora):
        self.__hora_salida = hora

    def set_hora_llegada(self, hora):
        self.__hora_llegada = hora

    def set_sector(self, sector):
        self.__sector = sector

    def confirmar(self):
        self.__confirmado = True

    def mostrar(self):
        estado = "Confirmada" if self.__confirmado else "Pendiente"
        print("Cliente:", self.__cliente.get_nombre())
        print("Hora salida:", self.__hora_salida)
        print("Hora llegada:", self.__hora_llegada)
        print("Sector:", self.__sector)
        print("Estado:", estado)