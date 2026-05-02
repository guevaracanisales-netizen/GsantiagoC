def validar_campos(func):
    def envoltura(*args, **kwargs):
        for arg in args[1:]:
            if isinstance(arg, str) and not arg.strip():
                raise ValueError("⚠ Los campos no pueden estar vacíos.")
        return func(*args, **kwargs)
    return envoltura

def log_accion(func):
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando: {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} ejecutado correctamente.")
        return resultado
    return envoltura

class Reserva:
    @validar_campos
    @log_accion
    def __init__(self, cliente, hora_salida, hora_llegada, sector):
        self.__cliente      = cliente
        self.__hora_salida  = hora_salida
        self.__hora_llegada = hora_llegada
        self.__sector       = sector
        self.__confirmado   = False
        self.__cancelada    = False

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

    def get_cancelada(self):
        return self.__cancelada

    def set_hora_salida(self, hora):
        self.__hora_salida = hora

    def set_hora_llegada(self, hora):
        self.__hora_llegada = hora

    def set_sector(self, sector):
        self.__sector = sector

    def confirmar(self):
        self.__confirmado = True

    def cancelar(self):
        self.__cancelada = True

    # *args: muestra solo los campos que le pidas
    def mostrar_detalles(self, *args):
        info = {
            "cliente":  self.__cliente.get_nombre(),
            "hora":     f"{self.__hora_salida} → {self.__hora_llegada}",
            "sector":   self.__sector,
            "estado":   "Confirmada" if self.__confirmado else "Cancelada" if self.__cancelada else "Pendiente",
        }
        for campo in args:
            if campo in info:
                print(f"{campo.capitalize()}: {info[campo]}")

    def mostrar(self):
        self.mostrar_detalles("cliente", "hora", "sector", "estado")