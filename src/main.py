import flet as ft
from models.cliente import Cliente
from models.reserva import Reserva
from data.database import guardar_cliente, guardar_reserva, cargar_clientes, cargar_reservas
from views.components import encabezado, tarjeta_reserva, NEGRO, GRIS, CLARO, BLANCO, BORDE

clientes = []
reservas = []
estado   = {"hora": None, "carro": None}

disponibilidad = {
    ("6:00", "Bogotá"):     ["ABC123", "DEF456"],
    ("6:30", "Psilago"):     ["GHI789"],
    ("7:00", "Tocaima"):      ["ABC123"],
    ("7:30", "Anapoima"):       ["JKL012"],
    ("8:00", "La Mesa"):      ["DEF456"],
    ("8:30", "Agua de Dios"): ["MNO345"],
}

hora_llegada_map = {
    "6:00": "10:00",
    "6:30": "7:00",
    "7:00": "7:40",
    "7:30": "9:30",
    "8:00": "9:00",
    "8:30": "9:00"

}

def main(page: ft.Page):
    page.title = "ReViTe"
    page.bgcolor = CLARO
    page.padding = 0
    page.scroll = "auto"

    clientes.extend(cargar_clientes())
    datos_reservas = cargar_reservas(clientes)

    txt_cedula      = ft.TextField(label="Cédula",             width=220, bgcolor=BLANCO, border_radius=8)
    txt_nombre      = ft.TextField(label="Nombre",             width=220, bgcolor=BLANCO, border_radius=8)
    txt_direccion   = ft.TextField(label="Dirección recogida", width=220, bgcolor=BLANCO, border_radius=8)
    txt_celular     = ft.TextField(label="Celular",            width=220, bgcolor=BLANCO, border_radius=8)
    txt_dir_llegada = ft.TextField(label="Dirección de llegada (donde lo dejan)",
                                   width=350, bgcolor=BLANCO, border_radius=8)
    lbl_error = ft.Text("", color="red", size=12)
    lbl_carro = ft.Text("Ningún carro seleccionado", italic=True, color=GRIS, size=12)

    destino = ft.RadioGroup(
        on_change=lambda e: actualizar_carros(),
        content=ft.Column([ft.Radio(value=v, label=v) for v in
            ["Bogotá","Psilago", "Tocaima", "Anapoima", "La Mesa", "Agua de Dios"]], spacing=2),
    )

    grid_carros = ft.Row(wrap=True, spacing=8, run_spacing=8)

    def actualizar_carros():
        lista = disponibilidad.get((estado["hora"], destino.value), [])
        estado["carro"] = None
        lbl_carro.value = "Ningún carro seleccionado"
        grid_carros.controls.clear()
        for placa in lista:
            def tap(e, p=placa):
                estado["carro"] = p
                lbl_carro.value = f"Seleccionado: {p}"
                for t in grid_carros.controls:
                    t.bgcolor = NEGRO if t.data == p else CLARO
                    t.content.controls[1].color = BLANCO if t.data == p else GRIS
                page.update()
            grid_carros.controls.append(ft.Container(
                data=placa, on_click=tap,
                bgcolor=CLARO, border_radius=10, border=ft.border.all(1, BORDE),
                padding=ft.padding.symmetric(horizontal=14, vertical=10),
                content=ft.Column([ft.Text("🚗", size=20),
                                   ft.Text(f"Placa: {placa}", size=11, color=GRIS)],
                                  horizontal_alignment="center", spacing=2),
            ))
        if not lista:
            grid_carros.controls.append(ft.Text("No hay carros.", color="red", italic=True, size=12))
        page.update()

    btns_hora = []
    def sel_hora(h):
        estado["hora"] = h
        for b in btns_hora:
            b.bgcolor = NEGRO if b.data == h else BLANCO
            b.content.color = BLANCO if b.data == h else NEGRO
        actualizar_carros()
        page.update()

    for h in ["6:00", "6:30", "7:00", "7:30", "8:00", "8:30"]:
        btns_hora.append(ft.Container(
            data=h, bgcolor=BLANCO, border_radius=8, border=ft.border.all(1, BORDE),
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            content=ft.Text(h, size=13, weight="bold", color=NEGRO),
            on_click=lambda e, hora=h: sel_hora(hora),
        ))

    lista_reservas = ft.Column(spacing=10)
    for r, dl in datos_reservas:
        lista_reservas.controls.append(tarjeta_reserva(r, dl))

    pantalla_form     = ft.Column(visible=True,  spacing=0)
    pantalla_reservas = ft.Column(visible=False, spacing=0)

    def ir_a_reservas(e):
        lbl_error.value = ""
        for val, msg in [
            (txt_cedula.value.strip(),      " Ingresa la cédula."),
            (txt_nombre.value.strip(),      " Ingresa el nombre."),
            (txt_dir_llegada.value.strip(), " Ingresa la dirección de llegada."),
            (estado["hora"],               " Selecciona un horario."),
            (destino.value,                " Selecciona un destino."),
            (estado["carro"],              " Selecciona un carro."),
        ]:
            if not val:
                lbl_error.value = msg; page.update(); return

        c = Cliente(txt_cedula.value.strip(), txt_nombre.value.strip(), len(clientes)+1)
        clientes.append(c)
        guardar_cliente(c)

        hora_llegada = hora_llegada_map.get(estado["hora"], "—")
        r = Reserva(c, estado["hora"], hora_llegada, destino.value)
        reservas.append(r)
        dl = txt_dir_llegada.value.strip()
        guardar_reserva(r, dl)

        lista_reservas.controls.append(tarjeta_reserva(r, dl))
        pantalla_form.visible = False
        pantalla_reservas.visible = True
        page.update()

    def volver(e):
        txt_cedula.value      = ""
        txt_nombre.value      = ""
        txt_direccion.value   = ""
        txt_celular.value     = ""
        txt_dir_llegada.value = ""
        estado["hora"]  = None
        estado["carro"] = None
        lbl_carro.value = "Ningún carro seleccionado"
        lbl_error.value = ""
        for b in btns_hora:
            b.bgcolor      = BLANCO
            b.content.color = NEGRO
        pantalla_form.visible     = True
        pantalla_reservas.visible = False
        page.update()

    btn_crear  = ft.ElevatedButton("Crear reserva →", on_click=ir_a_reservas, bgcolor=NEGRO, color=BLANCO)
    btn_volver = ft.ElevatedButton("← Volver",        on_click=volver,        bgcolor=NEGRO, color=BLANCO)

    pantalla_form.controls = [
        encabezado(),
        ft.Container(padding=ft.padding.all(28), content=ft.Column([
            ft.Text("AGENDA TU DESTINO", size=17, weight="bold", color=NEGRO),
            ft.Divider(color=BORDE, height=1),
            ft.Row([
                ft.Column([txt_cedula, txt_nombre, txt_direccion, txt_celular], spacing=10),
                ft.Container(bgcolor=BLANCO, border_radius=12, border=ft.border.all(1, BORDE),
                             width=110, height=140, padding=14,
                             content=ft.Column([ft.Text("📷", size=50),
                                                ft.Text("Foto", size=11, color=GRIS)],
                                               horizontal_alignment="center")),
            ], spacing=24),
            txt_dir_llegada,
            ft.Divider(color=BORDE, height=1),
            ft.Text("Horarios", size=14, weight="bold", color=NEGRO),
            ft.Row(btns_hora, spacing=8),
            ft.Divider(color=BORDE, height=1),
            ft.Row([
                ft.Container(bgcolor=BLANCO, border_radius=10, border=ft.border.all(1, BORDE), padding=14,
                             content=ft.Column([ft.Text("Destino", size=14, weight="bold", color=NEGRO), destino], spacing=6)),
                ft.Container(bgcolor=BLANCO, border_radius=10, border=ft.border.all(1, BORDE), padding=14, expand=True,
                             content=ft.Column([ft.Text("Carros disponibles", size=14, weight="bold", color=NEGRO),
                                                grid_carros, lbl_carro], spacing=8)),
            ], spacing=14, vertical_alignment="start"),
            lbl_error, btn_crear,
        ], spacing=16)),
    ]

    pantalla_reservas.controls = [
        encabezado(),
        ft.Container(padding=ft.padding.all(28), content=ft.Column([
            ft.Text("RESERVAS REALIZADAS", size=17, weight="bold", color=NEGRO),
            ft.Divider(color=BORDE, height=1),
            lista_reservas, btn_volver,
        ], spacing=16)),
    ]

    page.add(pantalla_form, pantalla_reservas)

ft.app(target=main)

