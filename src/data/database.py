import csv, os
from models.cliente import Cliente
from models.reserva import Reserva

def guardar_cliente(c):
    nuevo = not os.path.exists("clientes.csv")
    with open("clientes.csv", "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["id", "cedula", "nombre"])
        w.writerow([c.get_id_cliente(), c.get_cedula(), c.get_nombre()])

def guardar_reserva(r, dir_llegada):
    nuevo = not os.path.exists("reservas.csv")
    with open("reservas.csv", "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["cedula", "hora_salida", "hora_llegada", "sector", "dir_llegada"])
        w.writerow([r.get_cliente().get_cedula(), r.get_hora_salida(),
                    r.get_hora_llegada(), r.get_sector(), dir_llegada])

def cargar_clientes():
    if not os.path.exists("clientes.csv"):
        return []
    with open("clientes.csv", "r", encoding="utf-8") as f:
        return [Cliente(x["cedula"], x["nombre"], int(x["id"])) for x in csv.DictReader(f)]

def cargar_reservas(clientes):
    if not os.path.exists("reservas.csv"):
        return []
    with open("reservas.csv", "r", encoding="utf-8") as f:
        resultado = []
        for x in csv.DictReader(f):
            c = next((c for c in clientes if c.get_cedula() == x["cedula"]), None)
            if c:
                resultado.append((Reserva(c, x["hora_salida"], x.get("hora_llegada", "—"), x["sector"]),
                                  x.get("dir_llegada", "—")))
        return resultado