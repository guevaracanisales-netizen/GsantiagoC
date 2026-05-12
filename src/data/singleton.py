import sqlite3

class ConexionDB:
    _instancia = None  # ← guarda la única instancia

    def __new__(cls):
        # Si no existe instancia la crea — si ya existe devuelve la misma
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.conexion = sqlite3.connect("ReViTe.db", check_same_thread=False)
            print("[SINGLETON] Conexión creada.")
        else:
            print("[SINGLETON] Reutilizando conexión existente.")
        return cls._instancia

    def get_conexion(self):
        return self.conexion


# ── Prueba del patrón
if __name__ == "__main__":
    db1 = ConexionDB()
    db2 = ConexionDB()
    db3 = ConexionDB()

    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"db2 is db3: {db2 is db3}")  # True
    print("Las 3 variables apuntan a la misma instancia ✔")