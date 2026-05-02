import flet as ft
import shutil, os
from models.cliente import Cliente
from models.reserva import Reserva
from data.database import guardar_cliente, guardar_reserva, cargar_clientes, cargar_reservas, cargar_carros, crear_base_datos

crear_base_datos()
from views.components import encabezado, tarjeta_reserva, NEGRO, GRIS, CLARO, BLANCO, BORDE
from views.carros_view import vista_carros
from views.clientes_view import vista_clientes
from views.reservas_view import vista_reservas

clientes = []
reservas = []
carros   = []
estado   = {"hora": None, "carro": None, "foto": None, "cliente_actual": None}

disponibilidad = {
    ("6:00",  "Girardot"):     ["ABC123", "DEF456"],
    ("6:30",  "Girardot"):     ["GHI789"],
    ("6:00",  "Tocaima"):      ["ABC123"],
    ("7:00",  "Bogotá"):       ["JKL012"],
    ("7:30",  "La Mesa"):      ["DEF456"],
    ("8:00",  "Agua de Dios"): ["MNO345"],
    ("8:30",  "Girardot"):     ["ABC123"],
}

hora_llegada_map = {
    "6:00":  "7:00",
    "6:30":  "7:30",
    "7:00":  "8:00",
    "7:30":  "8:30",
    "8:00":  "9:00",
    "8:30":  "9:30",
}

def main(page: ft.Page):
    page.title = "ReViTe"
    page.bgcolor = CLARO
    page.padding = 0
    page.scroll = "auto"
    page.horizontal_alignment = "center"

    clientes.extend(cargar_clientes())
    carros.extend(cargar_carros())
    reservas.extend(cargar_reservas(clientes))

    txt_cedula    = ft.TextField(label="Cédula",             width=220, bgcolor=BLANCO, border_radius=8)
    txt_nombre    = ft.TextField(label="Nombre",             width=220, bgcolor=BLANCO, border_radius=8)
    txt_direccion = ft.TextField(label="Dirección recogida", width=220, bgcolor=BLANCO, border_radius=8)
    txt_celular   = ft.TextField(label="Celular",            width=220, bgcolor=BLANCO, border_radius=8)
    lbl_error1    = ft.Text("", color="red", size=12)

    img_foto   = ft.Image(src="", width=82, height=82, fit="cover", border_radius=8, visible=False)
    icono_foto = ft.Column([ft.Text("📷", size=50), ft.Text("Foto", size=11, color=GRIS)],
                           horizontal_alignment="center")

    def foto_seleccionada(e: ft.FilePickerResultEvent):
        if e.files:
            ruta = e.files[0].path
            os.makedirs("fotos", exist_ok=True)
            shutil.copy(ruta, os.path.join("fotos", e.files[0].name))
            estado["foto"] = ruta
            img_foto.src = ruta
            img_foto.visible = True
            icono_foto.visible = False
            page.update()

    file_picker = ft.FilePicker(on_result=foto_seleccionada)
    page.overlay.append(file_picker)
    page.update()

    caja_foto = ft.Container(
        bgcolor=BLANCO, border_radius=12, border=ft.border.all(1, BORDE),
        width=110, height=140, padding=14,
        on_click=lambda e: file_picker.pick_files(allowed_extensions=["jpg","jpeg","png"], allow_multiple=False),
        content=ft.Stack([icono_foto, img_foto]),
        tooltip="Clic para seleccionar foto",
    )

    campos_nuevos = ft.Column([txt_nombre, txt_direccion, txt_celular], spacing=10, visible=True)
    lbl_cliente_encontrado = ft.Text("", color="#2e7d32", size=12, weight="bold")

    txt_dir_llegada = ft.TextField(label="Dirección de llegada (donde lo dejan)",
                                   width=460, bgcolor=BLANCO, border_radius=8)
    lbl_error2     = ft.Text("", color="red", size=12)
    lbl_carro      = ft.Text("Ningún carro seleccionado", italic=True, color=GRIS, size=12)
    lbl_bienvenida = ft.Text("", size=14, color=NEGRO, weight="bold")

    destino = ft.RadioGroup(
        on_change=lambda e: actualizar_carros(),
        content=ft.Column([ft.Radio(value=v, label=v) for v in
            ["Girardot", "Tocaima", "Agua de Dios", "Bogotá", "La Mesa"]], spacing=2),
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
                data=placa, on_click=tap, bgcolor=CLARO, border_radius=10,
                border=ft.border.all(1, BORDE),
                padding=ft.padding.symmetric(horizontal=14, vertical=10),
                content=ft.Column([ft.Text("🚗", size=20), ft.Text(f"Placa: {placa}", size=11, color=GRIS)],
                                  horizontal_alignment="center", spacing=2),
            ))
        if not lista:
            grid_carros.controls.append(ft.Text("No hay carros para ese horario y destino.", color="red", italic=True, size=12))
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

    lista_reservas_ui = ft.Column(spacing=10, width=600)
    for r, dl in reservas:
        lista_reservas_ui.controls.append(tarjeta_reserva(r, dl))

    pantalla_paso1       = ft.Column(visible=True,  spacing=0, horizontal_alignment="center")
    pantalla_paso2       = ft.Column(visible=False, spacing=0, horizontal_alignment="center")
    pantalla_reservas    = ft.Column(visible=False, spacing=0, horizontal_alignment="center")
    pantalla_carros      = ft.Column(visible=False, spacing=0, horizontal_alignment="center")
    pantalla_clientes    = ft.Column(visible=False, spacing=0, horizontal_alignment="center")
    pantalla_reservas = ft.Column(visible=False, spacing=0, horizontal_alignment="center")

    def pasar_a_paso2(c):
        estado["cliente_actual"] = c
        lbl_bienvenida.value = f"Hola {c.get_nombre()}, elige tu viaje 👇"
        pantalla_paso1.visible = False
        pantalla_paso2.visible = True
        page.update()

    def on_cedula_change(e):
        cedula = txt_cedula.value.strip()
        cliente_existente = next((c for c in clientes if c.get_cedula() == cedula), None)
        if cliente_existente:
            txt_nombre.value = txt_direccion.value = txt_celular.value = ""
            campos_nuevos.visible = False
            lbl_cliente_encontrado.value = f"✅ Cliente encontrado: {cliente_existente.get_nombre()}"
        else:
            campos_nuevos.visible = True
            lbl_cliente_encontrado.value = ""
        lbl_error1.value = ""
        page.update()

    txt_cedula.on_change = on_cedula_change

    def ir_paso2(e):
        lbl_error1.value = ""
        cedula = txt_cedula.value.strip()
        if not cedula:
            lbl_error1.value = "⚠ Ingresa la cédula."; page.update(); return

        cliente_existente = next((c for c in clientes if c.get_cedula() == cedula), None)
        if cliente_existente:
            pasar_a_paso2(cliente_existente)
            return

        for val, msg in [
            (txt_nombre.value.strip(),    "⚠ Ingresa el nombre."),
            (txt_direccion.value.strip(), "⚠ Ingresa la dirección de recogida."),
            (txt_celular.value.strip(),   "⚠ Ingresa el celular."),
        ]:
            if not val:
                lbl_error1.value = msg; page.update(); return

        c = Cliente(cedula, txt_nombre.value.strip(), len(clientes)+1)
        clientes.append(c)
        guardar_cliente(c)
        pasar_a_paso2(c)

    def ir_a_reservas(e):
        lbl_error2.value = ""
        for val, msg in [
            (txt_dir_llegada.value.strip(), "⚠ Ingresa la dirección de llegada."),
            (estado["hora"],               "⚠ Selecciona un horario."),
            (destino.value,                "⚠ Selecciona un destino."),
            (estado["carro"],              "⚠ Selecciona un carro."),
        ]:
            if not val:
                lbl_error2.value = msg; page.update(); return

        c = estado["cliente_actual"]
        hora_llegada = hora_llegada_map.get(estado["hora"], "—")
        r = Reserva(c, estado["hora"], hora_llegada, destino.value)
        dl = txt_dir_llegada.value.strip()
        guardar_reserva(r, dl)
        reservas.append((r, dl))
        lista_reservas_ui.controls.append(tarjeta_reserva(r, dl))
        pantalla_paso2.visible    = False
        pantalla_reservas.visible = True
        page.update()

    def volver_a_inicio(e):
        txt_cedula.value = txt_nombre.value = txt_direccion.value = txt_celular.value = ""
        txt_dir_llegada.value = ""
        estado["hora"] = estado["carro"] = estado["foto"] = estado["cliente_actual"] = None
        lbl_carro.value = "Ningún carro seleccionado"
        lbl_error1.value = lbl_error2.value = ""
        lbl_cliente_encontrado.value = ""
        campos_nuevos.visible = True
        img_foto.src = ""; img_foto.visible = False; icono_foto.visible = True
        for b in btns_hora:
            b.bgcolor = BLANCO; b.content.color = NEGRO
        grid_carros.controls.clear()
        pantalla_reservas.visible     = False
        pantalla_paso2.visible        = False
        pantalla_reservas.visible = False
        pantalla_paso1.visible        = True
        page.update()

    def ir_a_carros(e):
        pantalla_paso1.visible  = False
        pantalla_carros.visible = True
        page.update()

    def volver_carros(e):
        pantalla_carros.visible = False
        pantalla_paso1.visible  = True
        page.update()

    def ir_a_clientes(e):
        pantalla_paso1.visible    = False
        pantalla_clientes.visible = True
        page.update()

    def volver_clientes(e):
        pantalla_clientes.visible = False
        pantalla_paso1.visible    = True
        page.update()

    def ir_a_mis_reservas(e):
        pantalla_reservas.visible     = False
        pantalla_reservas.visible = True
        pantalla_reservas.controls = [
            vista_reservas(page, reservas, estado["cliente_actual"], volver_mis_reservas)
        ]
        page.update()

    def volver_mis_reservas(e):
        pantalla_reservas.visible = False
        pantalla_reservas.visible     = True
        page.update()

    pantalla_carros.controls   = [vista_carros(page, carros, volver_carros)]
    pantalla_clientes.controls = [vista_clientes(page, clientes, volver_clientes)]

    pantalla_paso1.controls = [
        encabezado(),
        ft.Container(
            width=660, padding=ft.padding.all(28),
            content=ft.Column([
                ft.Row([
                    ft.Text("PASO 1 — Datos del cliente", size=17, weight="bold", color=NEGRO),
                    ft.Row([
                        ft.ElevatedButton("👤 Clientes", on_click=ir_a_clientes, bgcolor=GRIS, color=BLANCO),
                        ft.ElevatedButton("🚗 Carros",   on_click=ir_a_carros,   bgcolor=GRIS, color=BLANCO),
                    ], spacing=8),
                ], alignment="spaceBetween"),
                ft.Divider(color=BORDE, height=1),
                ft.Text("Si ya estás registrado solo ingresa tu cédula.", color=GRIS, size=12, italic=True),
                ft.Row([
                    ft.Column([txt_cedula, lbl_cliente_encontrado, campos_nuevos], spacing=10),
                    caja_foto,
                ], spacing=24, alignment="center"),
                lbl_error1,
                ft.ElevatedButton("Siguiente →", on_click=ir_paso2, bgcolor=NEGRO, color=BLANCO),
            ], spacing=16),
        ),
    ]

    pantalla_paso2.controls = [
        encabezado(),
        ft.Container(
            width=660, padding=ft.padding.all(28),
            content=ft.Column([
                ft.Text("PASO 2 — Elige tu viaje", size=17, weight="bold", color=NEGRO),
                ft.Divider(color=BORDE, height=1),
                lbl_bienvenida,
                txt_dir_llegada,
                ft.Text("Horarios", size=14, weight="bold", color=NEGRO),
                ft.Row(btns_hora, spacing=8, wrap=True),
                ft.Divider(color=BORDE, height=1),
                ft.Row([
                    ft.Container(bgcolor=BLANCO, border_radius=10, border=ft.border.all(1, BORDE), padding=14,
                                 content=ft.Column([ft.Text("Destino", size=14, weight="bold", color=NEGRO), destino], spacing=6)),
                    ft.Container(bgcolor=BLANCO, border_radius=10, border=ft.border.all(1, BORDE), padding=14, expand=True,
                                 content=ft.Column([ft.Text("Carros disponibles", size=14, weight="bold", color=NEGRO),
                                                    grid_carros, lbl_carro], spacing=8)),
                ], spacing=14, vertical_alignment="start"),
                lbl_error2,
                ft.Row([
                    ft.ElevatedButton("← Volver",       on_click=volver_a_inicio, bgcolor=GRIS,  color=BLANCO),
                    ft.ElevatedButton("Crear reserva →", on_click=ir_a_reservas,   bgcolor=NEGRO, color=BLANCO),
                ], spacing=10),
            ], spacing=16),
        ),
    ]

    pantalla_reservas.controls = [
        encabezado(),
        ft.Container(
            width=660, padding=ft.padding.all(28),
            content=ft.Column([
                ft.Text("✅ RESERVA CREADA", size=17, weight="bold", color=NEGRO),
                ft.Divider(color=BORDE, height=1),
                lista_reservas_ui,
                ft.Row([
                    ft.ElevatedButton("📋 Mis reservas",  on_click=ir_a_mis_reservas, bgcolor=GRIS,  color=BLANCO),
                    ft.ElevatedButton("← Nueva reserva", on_click=volver_a_inicio,   bgcolor=NEGRO, color=BLANCO),
                ], spacing=10),
            ], spacing=16),
        ),
    ]

    page.add(pantalla_paso1, pantalla_paso2, pantalla_reservas,
             pantalla_carros, pantalla_clientes, pantalla_reservas)

ft.app(target=main)

