from models.cliente import Cliente
from models.reserva import Reserva


class Store:
    def __init__(self):
        self.clientes: list[Cliente] = []
        self.reservas: list[Reserva] = []

    def add_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)

    def add_reserva(self, reserva: Reserva):
        self.reservas.append(reserva)

    def get_clientes(self):
        return list(self.clientes)

    def get_reservas(self):
        return list(self.reservas)
