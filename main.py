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

    # TAMANHO MOBILE
    page.window_width = 500
    page.window_height = 950

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
        scroll=ft.ScrollMode.AUTO,
        spacing=15
    )

    # =========================
    # CONTAINER CENTRAL
    # =========================

    container_central = ft.Container(
        content=body,
        width=550,
        padding=25,
        border_radius=25,
        bgcolor="white",
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color="#DADADA"
        )
    )

    # =========================
    # LAYOUT CENTRALIZADO
    # =========================

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Row(
                controls=[
                    container_central
                ],
                alignment=ft.MainAxisAlignment.CENTER
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
    # START LOGIN
    # =========================

    mostrar_login()


# =========================
# START APP
# =========================

ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    host="0.0.0.0",
    port=8080,
    assets_dir="assets"
)