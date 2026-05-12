import flet as ft
from models.carro import Carro
from data.database import guardar_carro, guardar_todos_carros

NEGRO  = "#1a1a1a"
GRIS   = "#5a5a5a"
BLANCO = "#ffffff"
BORDE  = "#cccccc"
ROJO   = "#c0392b"

def vista_carros(page: ft.Page, carros: list, on_volver):

    txt_placa  = ft.TextField(label="Placa",  width=200, bgcolor=BLANCO, border_radius=8)
    txt_modelo = ft.TextField(label="Modelo", width=200, bgcolor=BLANCO, border_radius=8)
    txt_anio   = ft.TextField(label="Año",    width=200, bgcolor=BLANCO, border_radius=8)
    txt_marca  = ft.TextField(label="Marca",  width=200, bgcolor=BLANCO, border_radius=8)
    lbl_error  = ft.Text("", color=ROJO, size=12)
    lista_ui   = ft.Column(spacing=10)

    dlg = ft.AlertDialog(modal=True, title=ft.Text("Editar Carro"))
    page.dialog = dlg

    def abrir_editar(e, c):
        ep     = ft.TextField(label="Placa",  value=c.get_placa(),  width=200, bgcolor=BLANCO, border_radius=8)
        em     = ft.TextField(label="Modelo", value=c.get_modelo(), width=200, bgcolor=BLANCO, border_radius=8)
        ea     = ft.TextField(label="Año",    value=c.get_anio(),   width=200, bgcolor=BLANCO, border_radius=8)
        emarca = ft.TextField(label="Marca",  value=c.get_marca(),  width=200, bgcolor=BLANCO, border_radius=8)

        def guardar(e):
            nueva_placa = ep.value.strip().upper()
            if any(x.get_placa().upper() == nueva_placa and x is not c for x in carros):
                dlg.open = False
                lbl_error.value = "⚠ Ya existe un carro con esa placa."
                page.update(); return
            c.set_placa(nueva_placa); c.set_modelo(em.value.strip())
            c.set_anio(ea.value.strip()); c.set_marca(emarca.value.strip())
            guardar_todos_carros(carros)
            dlg.open = False
            refrescar()

        dlg.content = ft.Column([ft.Row([ep, em], spacing=10), ft.Row([ea, emarca], spacing=10)], tight=True, spacing=10)
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.ElevatedButton("Guardar", on_click=guardar, bgcolor=NEGRO, color=BLANCO),
        ]
        dlg.open = True
        page.update()

    def tarjeta(c):
        def eliminar(e, carro=c):
            carros.remove(carro)
            guardar_todos_carros(carros)
            refrescar()

        return ft.Container(
            bgcolor=BLANCO, border_radius=12, padding=14,
            border=ft.border.all(1, BORDE),
            content=ft.Row([
                ft.Column([
                    ft.Text(f"🚗 {c.get_placa()}", weight="bold", color=NEGRO),
                    ft.Text(f"Marca: {c.get_marca()}  |  Modelo: {c.get_modelo()}  |  Año: {c.get_anio()}", color=GRIS, size=13),
                ], spacing=4, expand=True),
                ft.Row([
                    ft.IconButton(icon=ft.icons.EDIT_OUTLINED,  icon_color=NEGRO, on_click=lambda e, carro=c: abrir_editar(e, carro)),
                    ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_color=ROJO,  on_click=eliminar),
                ]),
            ], alignment="spaceBetween"),
        )

    def refrescar():
        lista_ui.controls.clear()
        for c in carros:
            lista_ui.controls.append(tarjeta(c))
        if not carros:
            lista_ui.controls.append(ft.Text("No hay carros.", color=GRIS, italic=True, size=12))
        page.update()

    def agregar(e):
        lbl_error.value = ""
        for val, msg in [
            (txt_placa.value.strip(),  "⚠ Ingresa la placa."),
            (txt_modelo.value.strip(), "⚠ Ingresa el modelo."),
            (txt_anio.value.strip(),   "⚠ Ingresa el año."),
            (txt_marca.value.strip(),  "⚠ Ingresa la marca."),
        ]:
            if not val:
                lbl_error.value = msg; page.update(); return

        if any(c.get_placa().upper() == txt_placa.value.strip().upper() for c in carros):
            lbl_error.value = "⚠ Ya existe un carro con esa placa."
            page.update(); return

        c = Carro(txt_placa.value.strip().upper(), txt_modelo.value.strip(),
                  txt_anio.value.strip(), txt_marca.value.strip())
        carros.append(c)
        guardar_carro(c)
        txt_placa.value = txt_modelo.value = txt_anio.value = txt_marca.value = ""
        refrescar()

    refrescar()

    return ft.Column([
        ft.Container(
            bgcolor=NEGRO,
            padding=ft.padding.symmetric(horizontal=28, vertical=16),
            content=ft.Row([
                ft.Image(src="https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=36, height=36),
                ft.Column([
                    ft.Text("ReViTe", size=20, weight="bold", color=BLANCO),
                    ft.Text("Gestión de Carros", size=11, color="#aaa"),
                ], spacing=0),
            ], spacing=10),
        ),
        ft.Container(
            padding=ft.padding.symmetric(horizontal=28, vertical=16),
            content=ft.Column([
                ft.Text("AGREGAR CARRO", size=17, weight="bold", color=NEGRO),
                ft.Divider(color=BORDE, height=1),
                ft.Row([txt_placa, txt_modelo], spacing=10),
                ft.Row([txt_anio,  txt_marca],  spacing=10),
                lbl_error,
                ft.ElevatedButton("Agregar +", on_click=agregar, bgcolor=NEGRO, color=BLANCO),
                ft.Divider(color=BORDE, height=1),
                ft.Text("CARROS REGISTRADOS", size=17, weight="bold", color=NEGRO),
                lista_ui,
                ft.ElevatedButton("← Volver", on_click=on_volver, bgcolor=NEGRO, color=BLANCO),
            ], spacing=10),
        ),
    ], spacing=0)