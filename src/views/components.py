import flet as ft

NEGRO  = "#1a1a1a"
GRIS   = "#5a5a5a"
CLARO  = "#f2f2f2"
BLANCO = "#ffffff"
BORDE  = "#cccccc"

def encabezado():
    return ft.Container(
        bgcolor=NEGRO,
        padding=ft.padding.symmetric(horizontal=28, vertical=16),
        content=ft.Row([
            ft.Text("🚗", size=22),
            ft.Column([
                ft.Text("ReViTe", size=20, weight="bold", color=BLANCO),
                ft.Text("Reservas de Viajes Terrestres", size=11, color="#aaa"),
            ], spacing=0),
        ], spacing=10),
    )

def tarjeta_reserva(r, dir_llegada="—"):
    confirmado   = r.get_confirmado()
    estado       = "✅ Confirmada" if confirmado else "⏳ Pendiente"
    estado_color = "#2e7d32" if confirmado else GRIS

    return ft.Container(
        bgcolor=BLANCO, border_radius=12, padding=14,
        border=ft.border.all(1, BORDE),
        content=ft.Column([
            ft.Text(r.get_cliente().get_nombre(), weight="bold", color=NEGRO),
            ft.Text(f"🕐 {r.get_hora_salida()} → {r.get_hora_llegada()}  📍 {r.get_sector()}",
                    color=GRIS, size=13),
            ft.Text(f"📌 Dejar en: {dir_llegada}", color=GRIS, size=13),
            ft.Text(estado, color=estado_color, size=12),
        ], spacing=4),
    )