import flet as ft

from auth import login
from components.buttons import (
    primary_button,
    success_button
)


def tela_login(
    page,
    usuario,
    atualizar,
    mostrar_cadastro
):

    # =========================
    # CAMPOS
    # =========================

    email = ft.TextField(
        label="Email",
        height=60,
        border_radius=18,
        prefix_icon=ft.Icons.EMAIL,
        filled=True,
        bgcolor="#F8FAFC",
        border_color="#E2E8F0",
        text_size=16
    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        height=60,
        border_radius=18,
        prefix_icon=ft.Icons.LOCK,
        filled=True,
        bgcolor="#F8FAFC",
        border_color="#E2E8F0",
        text_size=16
    )

    mensagem = ft.Text(
        color="red",
        size=14,
        weight=ft.FontWeight.W_500
    )

    # =========================
    # LOGIN
    # =========================

    def fazer_login(e):

        resultado = login(
            email.value,
            senha.value
        )

        # SUCESSO
        if resultado["sucesso"]:

            usuario["uid"] = resultado["usuario"]["uid"]
            usuario["nome"] = resultado["usuario"]["nome"]
            usuario["tipo"] = resultado["usuario"]["tipo"]

            atualizar()

        # ERRO
        else:

            mensagem.value = resultado["mensagem"]

            page.update()

    # =========================
    # UI
    # =========================

    return ft.Container(
        padding=20,

        content=ft.Column(
            spacing=25,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                # =========================
                # LOGO
                # =========================

                ft.Container(
                    margin=ft.margin.only(
                        top=20,
                        bottom=10
                    ),

                    content=ft.Image(
                        src="logo.png",
                        width=170,
                        height=170,
                        fit=ft.ImageFit.CONTAIN
                    )
                ),

                # =========================
                # TITULO
                # =========================

                ft.Text(
                    "Bem-vindo",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#1E293B",
                    text_align=ft.TextAlign.CENTER
                ),

                ft.Text(
                    "Entre na sua conta",
                    size=16,
                    color="#64748B",
                    text_align=ft.TextAlign.CENTER
                ),

                # =========================
                # FORMULÁRIO
                # =========================

                ft.Container(
                    width=420,

                    content=ft.Column(
                        spacing=18,

                        controls=[

                            email,

                            senha,

                            mensagem,

                            primary_button(
                                "Entrar",
                                fazer_login
                            ),

                            success_button(
                                "Criar conta",
                                mostrar_cadastro
                            )
                        ]
                    )
                )
            ]
        )
    )