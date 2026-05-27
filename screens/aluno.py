import flet as ft
from components.cards import card_horario_aluno
from components.buttons import primary_button
from database import (
    listar_horarios,
    reservar_horario,
    buscar_reserva_do_aluno,
    excluir_reserva
)


def tela_aluno(page, usuario, logout):
    conteudo = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # Guarda o último agendamento
    reserva_existente = buscar_reserva_do_aluno(usuario["uid"])

    ultimo_agendamento = {
    "data": reserva_existente["data"] if reserva_existente else None,
    "hora": reserva_existente["hora"] if reserva_existente else None
    }
    
    def cancelar_reserva(e):
        nonlocal ultimo_agendamento

        reserva = buscar_reserva_do_aluno(usuario["uid"])

        if reserva:
            excluir_reserva(reserva["id"])

            ultimo_agendamento = {
                "data": None,
                "hora": None
            }

            atualizar()


    def mostrar_msg(texto, cor="red"):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=cor
        )
        page.snack_bar.open = True
        page.update()

    def tela_confirmacao(horario):

        def confirmar(e):
            try:
                print("BOTÃO CONFIRMAR CLICADO")

                sucesso, msg = reservar_horario(
                    usuario["uid"],
                    usuario["nome"],
                    horario["id"]
                )

                print("RETORNO:", sucesso, msg)

                # Se reservou OU já tinha reservado
                if sucesso or "já reservou" in msg.lower():

                    # Salva o agendamento para mostrar no painel
                    ultimo_agendamento["data"] = horario["data"]
                    ultimo_agendamento["hora"] = horario["hora"]

                    # Fecha tela de confirmação
                    if len(page.views) > 1:
                        page.views.pop()

                    # Volta para tela principal
                    page.go("/")

                    # Atualiza painel
                    atualizar()

                    # Mensagem
                    if sucesso:
                        mostrar_msg("Reserva confirmada com sucesso!", "green")
                    else:
                        mostrar_msg(msg, "orange")

                else:
                    mostrar_msg(msg, "red")

            except Exception as erro:
                print("ERRO:", erro)
                mostrar_msg(f"Erro: {str(erro)}", "red")

        def cancelar(e):
            if len(page.views) > 1:
                page.views.pop()

            page.go("/")
            page.update()

        page.views.append(
            ft.View(
                route="/confirmar",
                controls=[
                    ft.Container(
                        expand=True,
                        padding=30,
                        bgcolor="#F5F7FB",
                        content=ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[

                                ft.Icon(
                                    ft.Icons.EVENT_AVAILABLE,
                                    size=90,
                                    color="#1E88E5"
                                ),

                                ft.Text(
                                    "Confirmar Reserva",
                                    size=30,
                                    weight="bold",
                                    color="#1E88E5"
                                ),

                                ft.Text(
                                    "Confira os dados da sua aula",
                                    size=16,
                                    color="grey"
                                ),

                                ft.Container(
                                    width=350,
                                    padding=25,
                                    border_radius=20,
                                    bgcolor="white",
                                    shadow=ft.BoxShadow(
                                        blur_radius=15,
                                        spread_radius=1,
                                        color="#DDDDDD"
                                    ),
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(
                                                f"📅 Data: {horario['data']}",
                                                size=20,
                                                weight="bold"
                                            ),
                                            ft.Text(
                                                f"⏰ Hora: {horario['hora']}",
                                                size=20
                                            ),
                                            ft.Text(
                                                f"👥 Vagas: {horario['vagas']}",
                                                size=20
                                            ),
                                        ]
                                    )
                                ),

                                primary_button(
                                    "Confirmar",
                                    confirmar
                                ),

                                ft.Container(height=10),

                                ft.ElevatedButton(
                                    "Cancelar",
                                    on_click=cancelar,
                                    bgcolor="#E53935",
                                    color="white"
                                )
                            ]
                        )
                    )
                ]
            )
        )

        page.update()

    def atualizar():
        conteudo.controls.clear()

        horarios = listar_horarios()
        lista = []

        if horarios:
            for h in horarios:
                lista.append(
                    card_horario_aluno(
                        h,
                        on_reservar=lambda h=h: tela_confirmacao(h)
                    )
                )
        else:
            lista.append(
                ft.Text("Nenhum horário disponível")
            )

        controles = [
            ft.Text(
                f"Olá, {usuario['nome']}",
                size=24,
                weight="bold",
                color="#43A047"
            ),
        ]

        # Painel mostrando último agendamento
        if ultimo_agendamento["data"]:
          conteudo.controls.append(
            ft.Card(
            content=ft.Container(
                padding=15,
                content=ft.Column(
                    [
                        ft.Text(
                            "Seu agendamento",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            f"Data: {ultimo_agendamento['data']}"
                        ),

                        ft.Text(
                            f"Hora: {ultimo_agendamento['hora']}"
                        ),

                        ft.ElevatedButton(
                            "Cancelar Reserva",
                            bgcolor="red",
                            color="white",
                            on_click=cancelar_reserva
                        )
                    ]
                )
            )
        )
    )

        controles.extend([
            ft.Text(
                "Escolha um horário para reservar",
                size=16,
                color="grey"
            ),

            *lista,

            ft.Divider(),

            primary_button(
                "Sair",
                lambda e: logout()
            )
        ])

        conteudo.controls.extend(controles)

        page.update()

    atualizar()

    return ft.Container(
        content=conteudo,
        padding=20,
        expand=True
    )