import flet as ft

NEGRO  = "#1a1a1a"
GRIS   = "#5a5a5a"
CLARO  = "#f2f2f2"
BLANCO = "#ffffff"
BORDE  = "#cccccc"

def encabezado():
    return ft.Container(
        bgcolor=NEGRO,
        width=float("inf"),
        padding=ft.padding.symmetric(horizontal=28, vertical=16),
        content=ft.Row([
            ft.Row([
                # ── Logo genérico de transporte
                ft.Image(
                    src="https://cdn-icons-png.flaticon.com/512/3063/3063822.png",
                    width=40,
                    height=40,
                ),
                ft.Column([
                    ft.Text("ReViTe", size=20, weight="bold", color=BLANCO),
                    ft.Text("Reservas de Viajes Terrestres", size=11, color="#aaa"),
                ], spacing=0),
            ], spacing=12),
        ], alignment="center"),
    )

def tarjeta_reserva(r, dir_llegada="—", on_cancelar=None):
    confirmado = r.get_confirmado()
    cancelada  = getattr(r, '_cancelada', False)

    if cancelada:
        estado       = "❌ Cancelada"
        estado_color = "#c0392b"
    elif confirmado:
        estado       = "✅ Confirmada"
        estado_color = "#2e7d32"
    else:
        estado       = "⏳ Pendiente"
        estado_color = GRIS

    controles = [
        ft.Text(r.get_cliente().get_nombre(), weight="bold", color=NEGRO),
        ft.Text(f"🕐 {r.get_hora_salida()} → {r.get_hora_llegada()}  📍 {r.get_sector()}",
                color=GRIS, size=13),
        ft.Text(f"📌 Dejar en: {dir_llegada}", color=GRIS, size=13),
        ft.Text(estado, color=estado_color, size=12),
    ]

    if on_cancelar and not cancelada and not confirmado:
        controles.append(
            ft.TextButton("Cancelar reserva", on_click=on_cancelar,
                         style=ft.ButtonStyle(color="#c0392b"))
        )

    return ft.Container(
        bgcolor=BLANCO, border_radius=12, padding=14,
        border=ft.border.all(1, BORDE),
        content=ft.Column(controles, spacing=4),
    )