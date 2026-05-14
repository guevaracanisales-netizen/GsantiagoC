# ARCHIVO DE PARÁMETROS — ReViTe 
# Aquí se centralizan todos los valores configurables de la app.
# Si quieres cambiar algo, solo lo cambias aquí y afecta todo el proyecto.

# información de la app
APP_NOMBRE    = "ReViTe"
APP_VERSION   = "1.0.0"
APP_SUBTITULO = "Reservas de Viajes Terrestres"

# base de datos
BD_NOMBRE = "ReViTe.db"

# horarios disponibles
HORARIOS = ["6:00", "6:30", "7:00", "7:30", "8:00", "8:30"]

# mapa de hora salida y hora llegada
HORA_LLEGADA_MAP = {
    "6:00": "7:00",
    "6:30": "7:30",
    "7:00": "10:00",
    "7:30": "8:30",
    "8:00": "9:00",
    "8:30": "9:30",
}

# sectores y destinos disponibles
SECTORES = ["Girardot", "Tocaima", "Agua de Dios", "Bogotá", "La Mesa"]

# disponibilidad de carros por horario y destino
DISPONIBILIDAD = {
    ("6:00", "Girardot"):     ["ABC123", "DEF456"],
    ("6:30", "Girardot"):     ["GHI789"],
    ("6:00", "Tocaima"):      ["ABC123"],
    ("7:00", "Bogotá"):       ["JKL012"],
    ("7:30", "La Mesa"):      ["DEF456"],
    ("8:00", "Agua de Dios"): ["MNO345"],
    ("8:30", "Girardot"):     ["ABC123"],
}

# capacidad
MAX_PASAJEROS_POR_CARRO = 4
MAX_CARROS_DIARIOS      = 5

# colores de la app
COLOR_NEGRO  = "#1a1a1a"
COLOR_GRIS   = "#5a5a5a"
COLOR_CLARO  = "#f2f2f2"
COLOR_BLANCO = "#ffffff"
COLOR_BORDE  = "#cccccc"
COLOR_ROJO   = "#c0392b"
COLOR_VERDE  = "#2e7d32"

# logo
LOGO_URL = r"C:\Users\USUARIO\Downloads\Gemini_Generated_Image_phrvuophrvuophrv.png" 
LOGO_SIZE = 36 