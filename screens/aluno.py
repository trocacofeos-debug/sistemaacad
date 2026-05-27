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
        expand=True,
        spacing=20
    )

    # =========================
    # RESERVA ATUAL
    # =========================

    reserva_existente = buscar_reserva_do_aluno(usuario["uid"])

    ultimo_agendamento = {
        "data": reserva_existente["data"] if reserva_existente else None,
        "hora": reserva_existente["hora"] if reserva_existente else None
    }

    # =========================
    # MENSAGEM
    # =========================

    def mostrar_msg(texto, cor="red"):

        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=cor
        )

        page.snack_bar.open = True
        page.update()

    # =========================
    # CANCELAR RESERVA
    # =========================

    def cancelar_reserva(e):

        nonlocal ultimo_agendamento

        reserva = buscar_reserva_do_aluno(
            usuario["uid"]
        )

        if reserva:

            excluir_reserva(reserva["id"])

            ultimo_agendamento = {
                "data": None,
                "hora": None
            }

            mostrar_msg(
                "Reserva cancelada!",
                "red"
            )

            atualizar()

    # =========================
    # TELA CONFIRMAÇÃO
    # =========================

    def tela_confirmacao(horario):

        def confirmar(e):

            try:

                sucesso, msg = reservar_horario(
                    usuario["uid"],
                    usuario["nome"],
                    horario["id"]
                )

                if sucesso or "já reservou" in msg.lower():

                    ultimo_agendamento["data"] = horario["data"]
                    ultimo_agendamento["hora"] = horario["hora"]

                    if len(page.views) > 1:
                        page.views.pop()

                    page.go("/")

                    atualizar()

                    if sucesso:

                        mostrar_msg(
                            "Reserva confirmada!",
                            "green"
                        )

                    else:

                        mostrar_msg(
                            msg,
                            "orange"
                        )

                else:

                    mostrar_msg(msg)

            except Exception as erro:

                mostrar_msg(
                    f"Erro: {str(erro)}"
                )

        def cancelar(e):

            if len(page.views) > 1:
                page.views.pop()

            page.go("/")
            page.update()

        page.views.append(

            ft.View(
                route="/confirmar",
                bgcolor="#F5F7FB",

                controls=[

                    ft.Container(
                        expand=True,
                        padding=20,

                        content=ft.Column(
                            expand=True,
                            spacing=25,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,

                            controls=[

                                ft.Icon(
                                    ft.Icons.EVENT_AVAILABLE,
                                    size=80,
                                    color="#1E88E5"
                                ),

                                ft.Text(
                                    "Confirmar Reserva",
                                    size=28,
                                    weight="bold",
                                    text_align="center",
                                    color="#1E88E5"
                                ),

                                ft.Text(
                                    "Confira os dados da aula",
                                    size=15,
                                    color="grey",
                                    text_align="center"
                                ),

                                # CARD
                                ft.Container(
                                    width=400,
                                    border_radius=25,
                                    bgcolor="white",
                                    padding=25,

                                    shadow=ft.BoxShadow(
                                        blur_radius=15,
                                        spread_radius=1,
                                        color="#DDDDDD"
                                    ),

                                    content=ft.Column(
                                        spacing=15,

                                        controls=[

                                            ft.Text(
                                                f"📅 {horario['data']}",
                                                size=20,
                                                weight="bold"
                                            ),

                                            ft.Text(
                                                f"⏰ {horario['hora']}",
                                                size=18
                                            ),

                                            ft.Text(
                                                f"👥 {horario['vagas']} vagas",
                                                size=18
                                            ),
                                        ]
                                    )
                                ),

                                # BOTÃO CONFIRMAR
                                primary_button(
                                    "Confirmar",
                                    confirmar
                                ),

                                # BOTÃO CANCELAR
                                ft.OutlinedButton(
                                    "Cancelar",
                                    width=320,
                                    height=52,
                                    on_click=cancelar,

                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=15
                                        ),

                                        color="#E53935"
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )

        page.update()

    # =========================
    # ATUALIZAR TELA
    # =========================

    def atualizar():

        conteudo.controls.clear()

        horarios = listar_horarios()

        lista_horarios = []

        # =========================
        # LISTA HORÁRIOS
        # =========================

        if horarios:

            for h in horarios:

                lista_horarios.append(

                    card_horario_aluno(
                        h,
                        on_reservar=lambda h=h: tela_confirmacao(h)
                    )
                )

        else:

            lista_horarios.append(

                ft.Container(
                    padding=20,
                    border_radius=20,
                    bgcolor="white",

                    content=ft.Text(
                        "Nenhum horário disponível",
                        text_align="center"
                    )
                )
            )

        # =========================
        # TOPO
        # =========================

        conteudo.controls.append(

            ft.Column(
                spacing=5,

                controls=[

                    ft.Text(
                        f"Olá, {usuario['nome']}",
                        size=28,
                        weight="bold",
                        color="#43A047"
                    ),

                    ft.Text(
                        "Escolha um horário para reservar",
                        size=16,
                        color="grey"
                    )
                ]
            )
        )

        # =========================
        # CARD AGENDAMENTO
        # =========================

        if ultimo_agendamento["data"]:

            conteudo.controls.append(

                ft.Container(
                    border_radius=25,
                    padding=20,
                    bgcolor="white",

                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        spread_radius=1,
                        color="#DDDDDD"
                    ),

                    content=ft.Column(
                        spacing=15,

                        controls=[

                            ft.Text(
                                "Seu Agendamento",
                                size=20,
                                weight="bold",
                                color="#1E88E5"
                            ),

                            ft.Text(
                                f"📅 {ultimo_agendamento['data']}",
                                size=17
                            ),

                            ft.Text(
                                f"⏰ {ultimo_agendamento['hora']}",
                                size=17
                            ),

                            ft.ElevatedButton(
                                "Cancelar Reserva",
                                width=220,
                                height=50,
                                bgcolor="#E53935",
                                color="white",
                                on_click=cancelar_reserva,

                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(
                                        radius=15
                                    )
                                )
                            )
                        ]
                    )
                )
            )

        # =========================
        # CARDS HORÁRIOS
        # =========================

        conteudo.controls.extend(
            lista_horarios
        )

        # =========================
        # SAIR
        # =========================

        conteudo.controls.append(

            ft.Container(
                margin=ft.margin.only(top=10),

                content=primary_button(
                    "Sair",
                    lambda e: logout()
                )
            )
        )

        page.update()

    atualizar()

    return ft.Container(
        expand=True,
        padding=20,
        content=conteudo
    )