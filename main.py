import flet as ft

from screens.login import tela_login
from screens.cadastro import tela_cadastro
from screens.admin import tela_admin
from screens.aluno import tela_aluno


def main(page: ft.Page):
    print("APP INICIOU")

    page.title = "Espaço Bem-Estar"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F7FB"
    page.scroll = ft.ScrollMode.AUTO

    usuario = {
        "uid": None,
        "nome": None,
        "tipo": None
    }

    # COLUNA PRINCIPAL
    body = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    # CONTAINER CENTRALIZADO
    container_central = ft.Container(
        content=body,
        width=420,
        padding=20,
        border_radius=20,
        bgcolor="white"
    )

    page.add(
        ft.Row(
            controls=[
                container_central
            ],
            alignment=ft.MainAxisAlignment.CENTER
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
        print("CARREGANDO LOGIN")

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
    # ATUALIZAR TELA
    # =========================

    def atualizar():
        body.controls.clear()

        try:
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

    mostrar_login()


# =========================
# START APP
# =========================

ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    port=8080,
    assets_dir="assets"
)