import flet as ft
from data.database import guardar_reserva  # o crear guardar_todas_reservas

NEGRO  = "#1a1a1a"
GRIS   = "#5a5a5a"
BLANCO = "#ffffff"
BORDE  = "#cccccc"
ROJO   = "#c0392b"
VERDE  = "#2e7d32"

def vista_reservas(page: ft.Page, reservas: list, on_volver):

    lista_ui = ft.Column(spacing=10)

    dlg = ft.AlertDialog(modal=True, title=ft.Text("Editar Reserva"))
    page.dialog = dlg

    # 🔄 REFRESCAR
    def refrescar():
        lista_ui.controls.clear()
        for r, dir_llegada in reservas:
            lista_ui.controls.append(tarjeta(r, dir_llegada))
        if not reservas:
            lista_ui.controls.append(ft.Text("No hay reservas.", color=GRIS, italic=True))
        page.update()

    # 🧾 TARJETA
    def tarjeta(r, dir_llegada):
        def eliminar(e):
            reservas.remove((r, dir_llegada))
            refrescar()

        def confirmar(e):
            r.confirmar()
            refrescar()

        return ft.Container(
            bgcolor=BLANCO,
            border_radius=12,
            padding=14,
            border=ft.border.all(1, BORDE),
            content=ft.Column([
                ft.Text(r.get_cliente().get_nombre(), weight="bold", color=NEGRO),
                ft.Text(f"{r.get_hora_salida()} → {r.get_hora_llegada()} | {r.get_sector()}"),
                ft.Text(f"📍 {dir_llegada}", size=12, color=GRIS),
                ft.Text(
                    "Confirmada" if r.get_confirmado() else "Pendiente",
                    color=VERDE if r.get_confirmado() else GRIS,
                    size=12
                ),
                ft.Row([
                    ft.IconButton(icon=ft.icons.CHECK, on_click=confirmar, icon_color=VERDE),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=eliminar, icon_color=ROJO),
                ])
            ])
        )

    refrescar()

    return ft.Column([
        ft.Container(
            bgcolor=NEGRO,
            padding=ft.padding.symmetric(horizontal=28, vertical=16),
            content=ft.Text("📋 Reservas", color=BLANCO, size=20)
        ),
        ft.Container(
            padding=ft.padding.all(28),
            content=ft.Column([
                lista_ui,
                ft.ElevatedButton("← Volver", on_click=on_volver, bgcolor=NEGRO, color=BLANCO)
            ])
        )
    ])