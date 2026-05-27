import flet as ft
from auth import login
from components.buttons import primary_button, success_button


def tela_login(page, usuario, atualizar, mostrar_cadastro):
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

    mensagem = ft.Text(color="red")

    def fazer_login(e):
        resultado = login(email.value, senha.value)

        if resultado["sucesso"]:
            usuario["uid"] = resultado["usuario"]["uid"]
            usuario["nome"] = resultado["usuario"]["nome"]
            usuario["tipo"] = resultado["usuario"]["tipo"]
            atualizar()
        else:
            mensagem.value = resultado["mensagem"]
            page.update()

    return ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[

                # LOGO
                ft.Image(
                    src="logo.png",
                    width=180,
                    height=180
                ),

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