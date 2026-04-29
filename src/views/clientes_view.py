import flet as ft
from data.database import guardar_todos_clientes

NEGRO  = "#1a1a1a"
GRIS   = "#5a5a5a"
CLARO  = "#f2f2f2"
BLANCO = "#ffffff"
BORDE  = "#cccccc"
ROJO   = "#c0392b"

def vista_clientes(page: ft.Page, clientes: list, on_volver):

    lista_ui = ft.Column(spacing=10, width=600)

    dlg = ft.AlertDialog(modal=True, title=ft.Text("Editar Cliente"))
    page.dialog = dlg

    def abrir_editar(e, c):
        ec = ft.TextField(label="Cédula", value=c.get_cedula(), width=200, bgcolor=BLANCO, border_radius=8)
        en = ft.TextField(label="Nombre", value=c.get_nombre(), width=200, bgcolor=BLANCO, border_radius=8)
        lbl_err = ft.Text("", color=ROJO, size=12)

        def guardar(e):
            nueva_cedula = ec.value.strip()
            if any(x.get_cedula() == nueva_cedula and x is not c for x in clientes):
                lbl_err.value = "⚠ Ya existe un cliente con esa cédula."
                page.update()
                return
            c.set_cedula(nueva_cedula)
            c.set_nombre(en.value.strip())
            guardar_todos_clientes(clientes)
            dlg.open = False
            refrescar()

        dlg.content = ft.Column([
            ft.Row([ec, en], spacing=10),
            lbl_err,
        ], tight=True, spacing=10)
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.ElevatedButton("Guardar", on_click=guardar, bgcolor=NEGRO, color=BLANCO),
        ]
        dlg.open = True
        page.update()

    def tarjeta(c):
        def eliminar(e, cliente=c):
            clientes.remove(cliente)
            guardar_todos_clientes(clientes)
            refrescar()

        return ft.Container(
            bgcolor=BLANCO, border_radius=12, padding=14,
            border=ft.border.all(1, BORDE),
            content=ft.Row([
                ft.Column([
                    ft.Text(f"👤 {c.get_nombre()}", weight="bold", color=NEGRO),
                    ft.Text(f"Cédula: {c.get_cedula()}", color=GRIS, size=13),
                ], spacing=4, expand=True),
                ft.Row([
                    ft.IconButton(icon=ft.icons.EDIT_OUTLINED,  icon_color=NEGRO, on_click=lambda e, cliente=c: abrir_editar(e, cliente)),
                    ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_color=ROJO,  on_click=eliminar),
                ]),
            ], alignment="spaceBetween"),
        )

    def refrescar():
        lista_ui.controls.clear()
        for c in clientes:
            lista_ui.controls.append(tarjeta(c))
        if not clientes:
            lista_ui.controls.append(
                ft.Text("No hay clientes registrados.", color=GRIS, italic=True, size=12))
        page.update()

    refrescar()

    return ft.Column([
        ft.Container(
            bgcolor=NEGRO,
            width=float("inf"),
            padding=ft.padding.symmetric(horizontal=28, vertical=16),
            content=ft.Row([
                ft.Row([
                    ft.Text("👤", size=22),
                    ft.Column([
                        ft.Text("ReViTe", size=20, weight="bold", color=BLANCO),
                        ft.Text("Clientes Registrados", size=11, color="#aaa"),
                    ], spacing=0),
                ], spacing=10),
            ], alignment="center"),
        ),
        ft.Container(
            width=660, padding=ft.padding.all(28),
            content=ft.Column([
                ft.Text("CLIENTES REGISTRADOS", size=17, weight="bold", color=NEGRO),
                ft.Divider(color=BORDE, height=1),
                lista_ui,
                ft.ElevatedButton("← Volver", on_click=on_volver, bgcolor=NEGRO, color=BLANCO),
            ], spacing=14),
        ),
    ], spacing=0, horizontal_alignment="center")