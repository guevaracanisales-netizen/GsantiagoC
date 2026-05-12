from models.pasajero import Pasajero

def validar_campos(func):
    def wrapper(*args, **kwargs):
        for arg in args[1:]:
            if isinstance(arg, str) and not arg.strip():
                raise ValueError("⚠ Los campos no pueden estar vacíos.")
        return func(*args, **kwargs)
    return wrapper

def log_accion(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Ejecutando: {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} ejecutado correctamente.")
        return resultado
    return wrapper

class Cliente(Pasajero):        
    @validar_campos
    @log_accion
    def __init__(self, cedula, nombre, id_cliente, direccion="", celular=""):
        super().__init__(cedula, nombre)   # ← llama al init del padre
        self.__id_cliente = id_cliente
        self.__direccion  = direccion
        self.__celular    = celular

    def get_id_cliente(self):
        return self.__id_cliente

    def get_direccion(self):
        return self.__direccion

    def get_celular(self):
        return self.__celular

    def set_id_cliente(self, id_cliente):
        self.__id_cliente = id_cliente

    def set_direccion(self, direccion):
        self.__direccion = direccion

    def set_celular(self, celular):
        self.__celular = celular

    def mostrar(self):           # ← implementa el método abstracto (polimorfismo)
        print("Cédula:",    self.get_cedula())
        print("Nombre:",    self.get_nombre())
        print("ID:",        self.__id_cliente)
        print("Dirección:", self.__direccion)
        print("Celular:",   self.__celular)

    def __str__(self):
        return self.get_nombre() + " - " + str(self.get_cedula())