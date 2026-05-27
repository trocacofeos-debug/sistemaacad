import flet as ft

from database import (
    adicionar_horario,
    listar_horarios,
    excluir_horario,
    listar_reservas_completas
)

from components.cards import card_horario_admin
from components.buttons import primary_button


def tela_admin(page, usuario, logout):

    conteudo = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=20
    )

    aba_atual = "horarios"

    # =========================
    # EXCLUIR HORÁRIO
    # =========================

    def apagar_horario(horario_id):

        excluir_horario(horario_id)

        atualizar()

    # =========================
    # TROCAR ABA
    # =========================

    def trocar_aba(nome):

        nonlocal aba_atual

        aba_atual = nome

        atualizar()

    # =========================
    # ATUALIZAR
    # =========================

    def atualizar():

        try:

            conteudo.controls.clear()

            # =========================
            # CAMPOS
            # =========================

            data = ft.TextField(
                label="Data",
                hint_text="Ex: 25/12/2026",
                expand=True,
                height=60,
                border_radius=18,
                prefix_icon=ft.Icons.CALENDAR_MONTH,
                filled=True,
                bgcolor="#F8FAFC",
                border_color="#E2E8F0",
                text_size=16
            )

            hora = ft.TextField(
                label="Hora",
                hint_text="Ex: 19:00",
                expand=True,
                height=60,
                border_radius=18,
                prefix_icon=ft.Icons.ACCESS_TIME,
                filled=True,
                bgcolor="#F8FAFC",
                border_color="#E2E8F0",
                text_size=16
            )

            vagas = ft.TextField(
                label="Quantidade de vagas",
                expand=True,
                height=60,
                border_radius=18,
                prefix_icon=ft.Icons.GROUPS,
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
            # SALVAR HORÁRIO
            # =========================

            def salvar_horario(e):

                if (
                    not data.value or
                    not hora.value or
                    not vagas.value
                ):

                    mensagem.value = "Preencha todos os campos"
                    mensagem.color = "red"

                    page.update()

                    return

                try:

                    adicionar_horario(
                        data.value,
                        hora.value,
                        int(vagas.value)
                    )

                    mensagem.value = "Horário salvo com sucesso!"
                    mensagem.color = "green"

                    atualizar()

                except:

                    mensagem.value = "Quantidade de vagas inválida"
                    mensagem.color = "red"

                    page.update()

            # =========================
            # TOPO
            # =========================

            conteudo.controls.append(

                ft.Container(
                    padding=20,
                    border_radius=25,
                    bgcolor="white",

                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        spread_radius=1,
                        color="#DDDDDD"
                    ),

                    content=ft.Column(
                        spacing=10,
                        controls=[

                            ft.Text(
                                f"Olá, {usuario['nome']}",
                                size=28,
                                weight="bold",
                                color="#1E88E5"
                            ),

                            ft.Text(
                                "Painel administrativo",
                                size=16,
                                color="grey"
                            )
                        ]
                    )
                )
            )

            # =========================
            # ABAS
            # =========================

            conteudo.controls.append(

                ft.ResponsiveRow(
                    controls=[

                        ft.Container(
                            col={"xs": 12, "sm": 6},
                            content=ft.ElevatedButton(
                                "Horários",
                                width=float("inf"),
                                height=52,

                                bgcolor=(
                                    "#1E88E5"
                                    if aba_atual == "horarios"
                                    else "#EAEAEA"
                                ),

                                color=(
                                    "white"
                                    if aba_atual == "horarios"
                                    else "black"
                                ),

                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(
                                        radius=15
                                    )
                                ),

                                on_click=lambda e: trocar_aba(
                                    "horarios"
                                )
                            )
                        ),

                        ft.Container(
                            col={"xs": 12, "sm": 6},
                            content=ft.ElevatedButton(
                                "Reservas",
                                width=float("inf"),
                                height=52,

                                bgcolor=(
                                    "#43A047"
                                    if aba_atual == "reservas"
                                    else "#EAEAEA"
                                ),

                                color=(
                                    "white"
                                    if aba_atual == "reservas"
                                    else "black"
                                ),

                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(
                                        radius=15
                                    )
                                ),

                                on_click=lambda e: trocar_aba(
                                    "reservas"
                                )
                            )
                        )
                    ]
                )
            )

            # =========================
            # ABA HORÁRIOS
            # =========================

            if aba_atual == "horarios":

                horarios = listar_horarios()

                lista_horarios = []

                if horarios:

                    for h in horarios:

                        lista_horarios.append(

                            card_horario_admin(
                                h,
                                on_delete=lambda horario_id=h["id"]: apagar_horario(
                                    horario_id
                                )
                            )
                        )

                else:

                    lista_horarios.append(

                        ft.Container(
                            padding=20,
                            border_radius=20,
                            bgcolor="white",

                            content=ft.Text(
                                "Nenhum horário cadastrado"
                            )
                        )
                    )

                # =========================
                # FORMULÁRIO
                # =========================

                conteudo.controls.append(

                    ft.Container(
                        padding=20,
                        border_radius=25,
                        bgcolor="white",

                        shadow=ft.BoxShadow(
                            blur_radius=12,
                            spread_radius=1,
                            color="#DDDDDD"
                        ),

                        content=ft.Column(
                            spacing=20,
                            controls=[

                                ft.Text(
                                    "Adicionar Horário",
                                    size=22,
                                    weight="bold"
                                ),

                                data,
                                hora,
                                vagas,
                                mensagem,

                                primary_button(
                                    "Salvar horário",
                                    salvar_horario
                                )
                            ]
                        )
                    )
                )

                # =========================
                # LISTA
                # =========================

                conteudo.controls.append(

                    ft.Text(
                        "Horários cadastrados",
                        size=22,
                        weight="bold"
                    )
                )

                conteudo.controls.extend(
                    lista_horarios
                )

            # =========================
            # ABA RESERVAS
            # =========================

            elif aba_atual == "reservas":

                reservas = listar_reservas_completas()

                grupos = {}

                for r in reservas:

                    chave = f"{r['data']} - {r['hora']}"

                    if chave not in grupos:
                        grupos[chave] = []

                    grupos[chave].append(
                        r["aluno_nome"]
                    )

                conteudo.controls.append(

                    ft.Text(
                        "Reservas dos alunos",
                        size=22,
                        weight="bold"
                    )
                )

                if grupos:

                    for horario, alunos in grupos.items():

                        lista_alunos = []

                        for nome in alunos:

                            lista_alunos.append(

                                ft.Container(
                                    padding=10,
                                    border_radius=12,
                                    bgcolor="#F5F7FB",

                                    content=ft.Text(
                                        f"• {nome}",
                                        size=15
                                    )
                                )
                            )

                        conteudo.controls.append(

                            ft.Container(
                                padding=20,
                                border_radius=25,
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
                                            horario,
                                            size=18,
                                            weight="bold",
                                            color="#1E88E5"
                                        ),

                                        ft.Divider(),

                                        *lista_alunos
                                    ]
                                )
                            )
                        )

                else:

                    conteudo.controls.append(

                        ft.Container(
                            padding=20,
                            border_radius=20,
                            bgcolor="white",

                            content=ft.Text(
                                "Nenhuma reserva encontrada"
                            )
                        )
                    )

            # =========================
            # BOTÃO SAIR
            # =========================

            conteudo.controls.append(

                ft.ElevatedButton(
                    "Sair",
                    on_click=lambda e: logout(),
                    width=float("inf"),
                    height=55,

                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=18
                        ),

                        bgcolor="#FD0000",
                        color="white",

                        text_style=ft.TextStyle(
                            size=16,
                            weight=ft.FontWeight.BOLD
                        )
                    )
                )
            )

            page.update()

        except Exception as e:

            print("ERRO ADMIN:", e)

    atualizar()

    return ft.Container(
        expand=True,
        padding=20,
        content=conteudo
    )