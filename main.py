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

    # RESPONSIVO
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
    # BODY PRINCIPAL
    # =========================

    body = ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # =========================
    # CONTAINER CENTRAL
    # =========================

    container_principal = ft.Container(
        content=body,

        # RESPONSIVO
        width=420,

        # IMPORTANTE
        expand=False,

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
    # LAYOUT CENTRALIZADO
    # =========================

    page.add(
        ft.Container(
            expand=True,
            padding=15,
            alignment=ft.alignment.top_center,

            content=ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        col={
                            "xs": 12,
                            "sm": 10,
                            "md": 8,
                            "lg": 6,
                            "xl": 4
                        },
                        controls=[
                            container_principal
                        ]
                    )
                ]
            )
        )
    )

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

ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    host="0.0.0.0",
    port=8080,
    assets_dir="assets"
)