import flet as ft
from auth import registrar
from components.buttons import primary_button, danger_button


def tela_cadastro(page, mostrar_login):
    nome = ft.TextField(
        label="Nome completo",
        width=320,
        border_radius=15,
        prefix_icon=ft.Icons.PERSON
    )

    telefone = ft.TextField(
        label="WhatsApp (ex: 21999999999)",
        width=320,
        border_radius=15,
        prefix_icon=ft.Icons.PHONE
    )

    email = ft.TextField(
        label="Email",
        width=320,
        border_radius=15,
        prefix_icon=ft.Icons.EMAIL
    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=320,
        border_radius=15,
        prefix_icon=ft.Icons.LOCK
    )

    mensagem = ft.Text()

    def cadastrar(e):
        if not nome.value or not telefone.value or not email.value or not senha.value:
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

        if resultado["sucesso"]:
            mensagem.value = "Conta criada com sucesso!"
            mensagem.color = "green"

            nome.value = ""
            telefone.value = ""
            email.value = ""
            senha.value = ""

        else:
            mensagem.value = resultado["mensagem"]
            mensagem.color = "red"

        page.update()

    return ft.Container(
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment="center",
            controls=[
                ft.Icon(
                    ft.Icons.PERSON_ADD,
                    size=80,
                    color="#43A047"
                ),

                ft.Text(
                    "Criar Conta",
                    size=28,
                    weight="bold",
                    color="#43A047"
                ),

                ft.Text(
                    "Cadastre-se no sistema",
                    size=16,
                    color="grey"
                ),

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
                ),
            ]
        ),
        padding=20
    )