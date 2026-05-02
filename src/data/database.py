import sqlite3
import os
from models.cliente import Cliente
from models.reserva import Reserva
from models.carro import Carro

nombre_bd = "ReViTe.db"

# ─── CREAR BASE DE DATOS ───
def crear_base_datos():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT UNIQUE NOT NULL,
                modelo TEXT NOT NULL,
                anio TEXT NOT NULL,
                marca TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT NOT NULL,
                hora_salida TEXT NOT NULL,
                hora_llegada TEXT NOT NULL,
                sector TEXT NOT NULL,
                dir_llegada TEXT NOT NULL,
                confirmada INTEGER DEFAULT 0,
                cancelada INTEGER DEFAULT 0,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conexion.commit()
        print(f"Base de datos '{nombre_bd}' y tablas creadas con éxito.")

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        if conexion:
            conexion.close()


# ─── CLIENTES ───
def insertar_cliente(cedula, nombre):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        sql = "INSERT INTO clientes (cedula, nombre) VALUES (?, ?)"
        cursor.execute(sql, (cedula, nombre))
        conexion.commit()
        print(f"Cliente '{nombre}' guardado correctamente.")
    except sqlite3.IntegrityError:
        print(f"Error: La cédula '{cedula}' ya está registrada.")
    except sqlite3.Error as e:
        print(f"Error al insertar cliente: {e}")
    finally:
        if conexion:
            conexion.close()

def consultar_clientes():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, cedula, nombre FROM clientes")
        filas = cursor.fetchall()
        if not filas:
            print("[!] La tabla 'clientes' está vacía.")
        else:
            for f in filas:
                print(*f)
    except sqlite3.Error as e:
        print(f"Error al consultar clientes: {e}")
    finally:
        if conexion:
            conexion.close()
    return [Cliente(f[1], f[2], f[0]) for f in filas] if filas else []

def eliminar_cliente(cedula):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE cedula = ?", (cedula,))
        conexion.commit()
        print(f"Cliente con cédula '{cedula}' eliminado.")
    except sqlite3.Error as e:
        print(f"Error al eliminar cliente: {e}")
    finally:
        if conexion:
            conexion.close()

def actualizar_cliente(cedula_actual, nueva_cedula, nuevo_nombre):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("UPDATE clientes SET cedula = ?, nombre = ? WHERE cedula = ?",
                       (nueva_cedula, nuevo_nombre, cedula_actual))
        conexion.commit()
        print(f"Cliente actualizado correctamente.")
    except sqlite3.Error as e:
        print(f"Error al actualizar cliente: {e}")
    finally:
        if conexion:
            conexion.close()


# ─── CARROS ───
def insertar_carro(placa, modelo, anio, marca):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        sql = "INSERT INTO carros (placa, modelo, anio, marca) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (placa, modelo, anio, marca))
        conexion.commit()
        print(f"Carro '{placa}' guardado correctamente.")
    except sqlite3.IntegrityError:
        print(f"Error: La placa '{placa}' ya está registrada.")
    except sqlite3.Error as e:
        print(f"Error al insertar carro: {e}")
    finally:
        if conexion:
            conexion.close()

def consultar_carros():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, placa, modelo, anio, marca FROM carros")
        filas = cursor.fetchall()
        if not filas:
            print("[!] La tabla 'carros' está vacía.")
        else:
            for f in filas:
                print(*f)
    except sqlite3.Error as e:
        print(f"Error al consultar carros: {e}")
    finally:
        if conexion:
            conexion.close()
    return [Carro(f[1], f[2], f[3], f[4]) for f in filas] if filas else []

def eliminar_carro(placa):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM carros WHERE placa = ?", (placa,))
        conexion.commit()
        print(f"Carro '{placa}' eliminado.")
    except sqlite3.Error as e:
        print(f"Error al eliminar carro: {e}")
    finally:
        if conexion:
            conexion.close()

def actualizar_carro(placa_actual, nueva_placa, modelo, anio, marca):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("UPDATE carros SET placa=?, modelo=?, anio=?, marca=? WHERE placa=?",
                       (nueva_placa, modelo, anio, marca, placa_actual))
        conexion.commit()
        print(f"Carro actualizado correctamente.")
    except sqlite3.Error as e:
        print(f"Error al actualizar carro: {e}")
    finally:
        if conexion:
            conexion.close()


# ─── RESERVAS ───
def insertar_reserva(cedula, hora_salida, hora_llegada, sector, dir_llegada):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        sql = "INSERT INTO reservas (cedula, hora_salida, hora_llegada, sector, dir_llegada) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, (cedula, hora_salida, hora_llegada, sector, dir_llegada))
        conexion.commit()
        print(f"Reserva guardada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al insertar reserva: {e}")
    finally:
        if conexion:
            conexion.close()

def consultar_reservas():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, cedula, hora_salida, hora_llegada, sector, dir_llegada, confirmada, cancelada FROM reservas")
        filas = cursor.fetchall()
        if not filas:
            print("[!] La tabla 'reservas' está vacía.")
        else:
            for f in filas:
                print(*f)
    except sqlite3.Error as e:
        print(f"Error al consultar reservas: {e}")
    finally:
        if conexion:
            conexion.close()
    return filas if filas else []

def cancelar_reserva_db(reserva_id):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("UPDATE reservas SET cancelada = 1 WHERE id = ?", (reserva_id,))
        conexion.commit()
        print(f"Reserva {reserva_id} cancelada.")
    except sqlite3.Error as e:
        print(f"Error al cancelar reserva: {e}")
    finally:
        if conexion:
            conexion.close()

def confirmar_reserva_db(reserva_id):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("UPDATE reservas SET confirmada = 1 WHERE id = ?", (reserva_id,))
        conexion.commit()
        print(f"Reserva {reserva_id} confirmada.")
    except sqlite3.Error as e:
        print(f"Error al confirmar reserva: {e}")
    finally:
        if conexion:
            conexion.close()


# ─── FUNCIONES COMPATIBLES CON EL MAIN ───
def guardar_cliente(c):
    insertar_cliente(c.get_cedula(), c.get_nombre())

def guardar_reserva(r, dir_llegada):
    insertar_reserva(r.get_cliente().get_cedula(), r.get_hora_salida(),
                     r.get_hora_llegada(), r.get_sector(), dir_llegada)

def guardar_carro(c):
    insertar_carro(c.get_placa(), c.get_modelo(), c.get_anio(), c.get_marca())

def guardar_todos_carros(carros):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM carros")
        for c in carros:
            cursor.execute("INSERT INTO carros (placa, modelo, anio, marca) VALUES (?, ?, ?, ?)",
                           (c.get_placa(), c.get_modelo(), c.get_anio(), c.get_marca()))
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al guardar carros: {e}")
    finally:
        if conexion:
            conexion.close()

def guardar_todos_clientes(clientes):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes")
        for c in clientes:
            cursor.execute("INSERT INTO clientes (cedula, nombre) VALUES (?, ?)",
                           (c.get_cedula(), c.get_nombre()))
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al guardar clientes: {e}")
    finally:
        if conexion:
            conexion.close()

def guardar_todas_reservas(reservas):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM reservas")
        for r, dl in reservas:
            cursor.execute(
                "INSERT INTO reservas (cedula, hora_salida, hora_llegada, sector, dir_llegada, confirmada, cancelada) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (r.get_cliente().get_cedula(), r.get_hora_salida(), r.get_hora_llegada(),
                 r.get_sector(), dl, int(r.get_confirmado()), int(r.get_cancelada()))
            )
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al guardar reservas: {e}")
    finally:
        if conexion:
            conexion.close()

def cargar_clientes():
    return consultar_clientes()

def cargar_carros():
    return consultar_carros()
def cargar_reservas(clientes):
    filas = consultar_reservas()
    resultado = []
    for f in filas:
        c = next((c for c in clientes if c.get_cedula() == f[1]), None)
        if c:
            r = Reserva(c, f[2], f[3], f[4])
            if f[7]: r.cancelar()
            if f[6]: r.confirmar()
            resultado.append((r, f[5]))
    return resultado


if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos aquí:")
    print(os.path.abspath(nombre_bd)) 