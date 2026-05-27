import flet as ft

from screens.login import tela_login
from screens.cadastro import tela_cadastro
from screens.admin import tela_admin
from screens.aluno import tela_aluno


def main(page: ft.Page):

    # =========================
    # CONFIG PAGE
    # =========================

    page.title = "Espaço Bem-Estar"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F7FB"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    # MOBILE
    page.window_width = 400
    page.window_height = 850
    page.window_min_width = 320
    page.window_min_height = 600

    # =========================
    # USUARIO
    # =========================

    usuario = {
        "uid": None,
        "nome": None,
        "tipo": None
    }

    # =========================
    # BODY
    # =========================

    body = ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # =========================
    # CONTAINER PRINCIPAL
    # =========================

    container_principal = ft.Container(
        content=body,
        padding=20,
        border_radius=25,
        bgcolor="white",

        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color="#DDDDDD"
        )
    )

    # =========================
    # LAYOUT
    # =========================

    layout = ft.Container(
        expand=True,
        bgcolor="#F5F7FB",
        padding=10,
        alignment=ft.Alignment(0, -1),

        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,

            controls=[

                ft.Container(
                    content=container_principal,

                    width=min(
                        page.window_width * 0.95,
                        430
                    ),

                    animate=300,
                )

            ]
        )
    )

    page.add(layout)

    # =========================
    # RESPONSIVIDADE
    # =========================

    def on_resize(e):

        layout.content.controls[0].width = min(
            page.window_width * 0.95,
            430
        )

        page.update()

    page.on_resize = on_resize

    # =========================
    # LOGOUT
    # =========================

    def logout():

        usuario["uid"] = None
        usuario["nome"] = None
        usuario["tipo"] = None

        mostrar_login()

    # =========================
    # LOGIN
    # =========================

    def mostrar_login():

        body.controls.clear()

        body.controls.append(
            tela_login(
                page=page,
                usuario=usuario,
                atualizar=atualizar,
                mostrar_cadastro=mostrar_cadastro
            )
        )

        page.update()

    # =========================
    # CADASTRO
    # =========================

    def mostrar_cadastro():

        body.controls.clear()

        body.controls.append(
            tela_cadastro(
                page=page,
                mostrar_login=mostrar_login
            )
        )

        page.update()

    # =========================
    # ATUALIZAR
    # =========================

    def atualizar():

        body.controls.clear()

        # NÃO LOGADO
        if not usuario["uid"]:

            mostrar_login()
            return

        # ADMIN
        if usuario["tipo"] == "admin":

            body.controls.append(
                tela_admin(
                    page=page,
                    usuario=usuario,
                    logout=logout
                )
            )

        # ALUNO
        else:

            body.controls.append(
                tela_aluno(
                    page=page,
                    usuario=usuario,
                    logout=logout
                )
            )

        page.update()

    # =========================
    # START
    # =========================

    mostrar_login()


# =========================
# APP
# =========================

ft.app(target=main,)