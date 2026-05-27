import flet as ft

from auth import registrar

from components.buttons import (
    primary_button,
    danger_button
)


def tela_cadastro(
    page,
    mostrar_login
):

    # =========================
    # CAMPOS
    # =========================

    nome = ft.TextField(
        label="Nome completo",
        height=60,
        border_radius=18,
        prefix_icon=ft.Icons.PERSON,
        filled=True,
        bgcolor="#F8FAFC",
        border_color="#E2E8F0",
        text_size=16
    )

    telefone = ft.TextField(
        label="WhatsApp",
        hint_text="21999999999",
        height=60,
        border_radius=18,
        prefix_icon=ft.Icons.PHONE,
        filled=True,
        bgcolor="#F8FAFC",
        border_color="#E2E8F0",
        text_size=16
    )

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
        size=14,
        weight=ft.FontWeight.W_500
    )

    # =========================
    # CADASTRAR
    # =========================

    def cadastrar(e):

        if (
            not nome.value
            or not telefone.value
            or not email.value
            or not senha.value
        ):

            mensagem.value = "Preencha todos os campos"
            mensagem.color = "red"

            page.update()

            return

        resultado = registrar(
            nome.value,
            telefone.value,
            email.value,
            senha.value
        )

        # SUCESSO
        if resultado["sucesso"]:

            mensagem.value = "Conta criada com sucesso!"
            mensagem.color = "green"

            nome.value = ""
            telefone.value = ""
            email.value = ""
            senha.value = ""

        # ERRO
        else:

            mensagem.value = resultado["mensagem"]
            mensagem.color = "red"

        page.update()

    # =========================
    # UI
    # =========================

    return ft.Container(
        expand=True,
        bgcolor="white",
        padding=20,

        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                # =========================
                # ÍCONE
                # =========================

                ft.Container(
                    margin=ft.Margin(0, 20, 0, 0),

                    padding=20,
                    border_radius=100,
                    bgcolor="#DCFCE7",

                    content=ft.Icon(
                        ft.Icons.PERSON_ADD,
                        size=70,
                        color="#16A34A"
                    )
                ),

                # =========================
                # TITULO
                # =========================

                ft.Text(
                    "Criar Conta",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#1E293B",
                    text_align=ft.TextAlign.CENTER
                ),

                ft.Text(
                    "Cadastre-se para acessar o sistema",
                    size=16,
                    color="#64748B",
                    text_align=ft.TextAlign.CENTER
                ),

                # =========================
                # FORM
                # =========================

                ft.Container(
                    width=float("inf"),
                    bgcolor="white",

                    content=ft.Column(
                        spacing=18,

                        controls=[

                            nome,

                            telefone,

                            email,

                            senha,

                            mensagem,

                            primary_button(
                                "Cadastrar",
                                cadastrar
                            ),

                            danger_button(
                                "Voltar para login",
                                lambda e: mostrar_login()
                            )
                        ]
                    )
                )
            ]
        )
    )