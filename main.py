import os
import flet as ft

from screens.login import tela_login
from screens.cadastro import tela_cadastro
from screens.admin import tela_admin
from screens.aluno import tela_aluno


def main(page: ft.Page):
    print("APP INICIOU")

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
    page.window_height = 800

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
        scroll=ft.ScrollMode.AUTO,
        spacing=20
    )

    # =========================
    # CONTAINER RESPONSIVO
    # =========================

    container_central = ft.Container(
        content=body,
        expand=True,
        padding=20,
        border_radius=0,
        bgcolor="white"
    )

    # =========================
    # LAYOUT
    # =========================

    layout = ft.Container(
        expand=True,
        bgcolor="#F5F7FB",
        content=ft.Row(
            [
                ft.Container(
                    content=container_central,
                    expand=True,
                    alignment=ft.Alignment(0, 0)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

    page.add(layout)

    # =========================
    # RESPONSIVIDADE
    # =========================

    def on_resize(e):

        largura = page.window_width

        # CELULAR
        if largura <= 600:

            container_central.width = largura
            container_central.border_radius = 0
            container_central.padding = 15

        # TABLET
        elif largura <= 900:

            container_central.width = 700
            container_central.border_radius = 20
            container_central.padding = 25

        # DESKTOP
        else:

            container_central.width = 500
            container_central.border_radius = 25
            container_central.padding = 30

        page.update()

    page.on_resized = on_resize

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

        try:

            body.controls.append(
                tela_login(
                    page=page,
                    usuario=usuario,
                    atualizar=atualizar,
                    mostrar_cadastro=mostrar_cadastro
                )
            )

            page.update()

        except Exception as e:
            print("ERRO LOGIN:", e)

    # =========================
    # CADASTRO
    # =========================

    def mostrar_cadastro():

        body.controls.clear()

        try:

            body.controls.append(
                tela_cadastro(
                    page=page,
                    mostrar_login=mostrar_login
                )
            )

            page.update()

        except Exception as e:
            print("ERRO CADASTRO:", e)

    # =========================
    # ATUALIZAR
    # =========================

    def atualizar():

        body.controls.clear()

        try:

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

        except Exception as e:
            print("ERRO ATUALIZAR:", e)

    # =========================
    # START
    # =========================

    on_resize(None)

    mostrar_login()


# =========================
# APP
# =========================

ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
    assets_dir="assets"
)