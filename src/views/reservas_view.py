import flet as ft

NEGRO  = "#1a1a1a"
GRIS   = "#5a5a5a"
BLANCO = "#ffffff"
BORDE  = "#cccccc"
ROJO   = "#c0392b"
VERDE  = "#2e7d32"

def vista_reservas(page: ft.Page, reservas: list, cliente_actual, on_volver):

    lista_ui = ft.Column(spacing=6)

    def refrescar():
        lista_ui.controls.clear()
        for r, dir_llegada in reservas:
            lista_ui.controls.append(tarjeta(r, dir_llegada))
        if not reservas:
            lista_ui.controls.append(ft.Text("No hay reservas.", color=GRIS, italic=True))
        page.update()

    def tarjeta(r, dir_llegada):
        def eliminar(e):
            reservas.remove((r, dir_llegada))
            refrescar()

        def confirmar(e):
            r.confirmar()
            refrescar()

        return ft.Container(
            bgcolor=BLANCO, border_radius=10, padding=10,
            border=ft.border.all(1, BORDE),
            content=ft.Column([
                ft.Text(r.get_cliente().get_nombre(), weight="bold", color=NEGRO, size=13),
                ft.Text(f"{r.get_hora_salida()} → {r.get_hora_llegada()} | {r.get_sector()}", size=12),
                ft.Text(f"📍 {dir_llegada}", size=12, color=GRIS),
                ft.Row([
                    ft.Text("Confirmada" if r.get_confirmado() else "Pendiente",
                            color=VERDE if r.get_confirmado() else GRIS, size=12),
                    ft.IconButton(icon=ft.icons.CHECK,  on_click=confirmar, icon_color=VERDE),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=eliminar,  icon_color=ROJO),
                ], spacing=4),
            ], spacing=2),
        )

    refrescar()

    return ft.Column([
        ft.Container(
            bgcolor=NEGRO,
            padding=ft.padding.symmetric(horizontal=28, vertical=14),
            content=ft.Row([
                ft.Image(src="https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=36, height=36),
                ft.Column([
                    ft.Text("ReViTe", size=20, weight="bold", color=BLANCO),
                    ft.Text("Mis Reservas", size=11, color="#aaa"),
                ], spacing=0),
            ], spacing=10),
        ),
        ft.Container(
            padding=ft.padding.symmetric(horizontal=28, vertical=12),
            content=ft.Column([
                ft.Text("RESERVAS REALIZADAS", size=15, weight="bold", color=NEGRO),
                ft.Divider(color=BORDE, height=1),
                lista_ui,
                ft.ElevatedButton("← Volver", on_click=on_volver, bgcolor=NEGRO, color=BLANCO),
            ], spacing=8),
        ),
    ])