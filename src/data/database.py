import json, os
from models.cliente import Cliente
from models.reserva import Reserva
from models.carro import Carro

ARCHIVO_CLIENTES = "clientes.json"
ARCHIVO_RESERVAS = "reservas.json"
ARCHIVO_CARROS   = "carros.json"

def guardar_cliente(c):
    datos = _leer_json(ARCHIVO_CLIENTES)
    datos.append({"id": c.get_id_cliente(), "cedula": c.get_cedula(), "nombre": c.get_nombre()})
    _escribir_json(ARCHIVO_CLIENTES, datos)

def guardar_todos_clientes(clientes):
    _escribir_json(ARCHIVO_CLIENTES, [
        {"id": c.get_id_cliente(), "cedula": c.get_cedula(), "nombre": c.get_nombre()}
        for c in clientes
    ])

def guardar_reserva(r, dir_llegada):
    datos = _leer_json(ARCHIVO_RESERVAS)
    datos.append({"cedula": r.get_cliente().get_cedula(), "hora_salida": r.get_hora_salida(),
                  "hora_llegada": r.get_hora_llegada(), "sector": r.get_sector(), "dir_llegada": dir_llegada})
    _escribir_json(ARCHIVO_RESERVAS, datos)

def guardar_todas_reservas(reservas):
    _escribir_json(ARCHIVO_RESERVAS, [
        {
            "cedula":       r.get_cliente().get_cedula(),
            "hora_salida":  r.get_hora_salida(),
            "hora_llegada": r.get_hora_llegada(),
            "sector":       r.get_sector(),
            "dir_llegada":  dl,
        }
        for r, dl in reservas
    ])

def guardar_carro(c):
    datos = _leer_json(ARCHIVO_CARROS)
    datos.append({"placa": c.get_placa(), "modelo": c.get_modelo(), "anio": c.get_anio(), "marca": c.get_marca()})
    _escribir_json(ARCHIVO_CARROS, datos)

def guardar_todos_carros(carros):
    _escribir_json(ARCHIVO_CARROS, [
        {"placa": c.get_placa(), "modelo": c.get_modelo(), "anio": c.get_anio(), "marca": c.get_marca()}
        for c in carros
    ])

def cargar_clientes():
    return [Cliente(x["cedula"], x["nombre"], int(x["id"])) for x in _leer_json(ARCHIVO_CLIENTES)]

def cargar_reservas(clientes):
    resultado = []
    for x in _leer_json(ARCHIVO_RESERVAS):
        c = next((c for c in clientes if c.get_cedula() == x["cedula"]), None)
        if c:
            resultado.append((Reserva(c, x["hora_salida"], x.get("hora_llegada", "-"), x["sector"]),
                              x.get("dir_llegada", "-")))
    return resultado

def cargar_carros():
    return [Carro(x["placa"], x["modelo"], x["anio"], x["marca"]) for x in _leer_json(ARCHIVO_CARROS)]

def _leer_json(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def _escribir_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)