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

class Carro:
    @validar_campos
    @log_accion
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

    # **kwargs: actualiza solo los atributos que le pases
    def actualizar(self, **kwargs):
        if "placa"  in kwargs: self.__placa  = kwargs["placa"]
        if "modelo" in kwargs: self.__modelo = kwargs["modelo"]
        if "anio"   in kwargs: self.__anio   = kwargs["anio"]
        if "marca"  in kwargs: self.__marca  = kwargs["marca"]
        print(f"[LOG] Carro {self.__placa} actualizado con: {kwargs}")

    def mostrar(self):
        print("Placa:",  self.__placa)
        print("Modelo:", self.__modelo)
        print("Año:",    self.__anio)
        print("Marca:",  self.__marca)

    def __str__(self):
        return f"{self.__placa} - {self.__marca} {self.__modelo} ({self.__anio})"