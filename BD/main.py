import sqlite3
import os

nombre_bd = "Revite.db"

def crear_base_datos():
    try:
        conexion = sqlite3.connect(nombre_bd)

        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT UNIQUE NOT NULL,
                celular TEXT NOT NULL,
                nombre TEXT NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conexion.commit()

        print(f"Base de datos '{nombre_bd}' y tabla de 'usuarios' creada con éxito.")

    except sqlite3.Error as e:
        print(f"Error al conectar o crear la base de datos: {e}")
    

def insertar_usuario(nombre, correo, cedula, celular):
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()

        sql = "INSERT INTO usuarios (nombre, correo, cedula, celular) VALUES (?, ?, ?, ?)"
        valores = (nombre, correo, cedula, celular)

        cursor.execute(sql, valores)
        conexion.commit()
        print(f"Usuario '{nombre}' guarado correctamente")

    except sqlite3.IntegrityError:
        print(f"Error: El correo '{correo}' ya está registrado")
    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")

def consultar_usuarios():
    try:
        conexion = sqlite3.connect(nombre_bd)
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, correo, cedula, celular, fecha_registro FROM usuarios"
        cursor.execute(sql)
        usuarios = cursor.fetchall()

        if not usuarios:
            print("\n[!] la tabla 'usuarios' está vacía.")
        else:
            for u in usuarios:
                print(*u)
    
    except sqlite3.Error as e:
        print(f"Error al consultar datos: {e}")
    finally:
        if conexion:
            conexion.close()
    return usuarios

if __name__ == "__main__":
    crear_base_datos()
    print("tu base de datos esta aquí")
    print(os.path.abspath(nombre_bd))
    insertar_usuario("pedro", "pedrito@gmail.com","11324000","3156789200")
    insertar_usuario("maria", "maria@gmail.com","11324000","3156789200")
    insertar_usuario("jose", "jose@gmail.com","11324000","3156789200")
    consultar_usuarios() 
