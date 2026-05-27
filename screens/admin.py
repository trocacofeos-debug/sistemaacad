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
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    aba_atual = "horarios"

    def apagar_horario(horario_id):
        excluir_horario(horario_id)
        atualizar()

    def trocar_aba(nome):
        nonlocal aba_atual
        aba_atual = nome
        atualizar()

    def atualizar():
        try:
            conteudo.controls.clear()

            # -------------------------
            # CAMPOS
            # -------------------------
            data = ft.TextField(
                label="Data (ex: 25/12/2025)",
                width=320
            )

            hora = ft.TextField(
                label="Hora (ex: 19:00)",
                width=320
            )

            vagas = ft.TextField(
                label="Quantidade de vagas",
                width=320
            )

            mensagem = ft.Text()

            def salvar_horario(e):
                if not data.value or not hora.value or not vagas.value:
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

                    mensagem.value = "Horário salvo com sucesso"
                    mensagem.color = "green"
                    atualizar()

                except:
                    mensagem.value = "Vagas deve ser número"
                    mensagem.color = "red"
                    page.update()

            # -------------------------
            # TOPO
            # -------------------------
            conteudo.controls.append(
                ft.Text(
                    f"Olá, {usuario['nome']} (Admin)",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#1E88E5"
                )
            )

            conteudo.controls.append(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Horários",
                            on_click=lambda e: trocar_aba("horarios")
                        ),
                        ft.ElevatedButton(
                            "Reservas",
                            on_click=lambda e: trocar_aba("reservas")
                        )
                    ]
                )
            )

            conteudo.controls.append(ft.Divider())

            # -------------------------
            # ABA HORÁRIOS
            # -------------------------
            if aba_atual == "horarios":
                horarios = listar_horarios()
                lista_horarios = []

                if horarios:
                    for h in horarios:
                        lista_horarios.append(
                            card_horario_admin(
                                h,
                                on_delete=lambda e, horario_id=h["id"]: apagar_horario(horario_id)
                            )
                        )
                else:
                    lista_horarios.append(
                        ft.Text("Nenhum horário cadastrado")
                    )

                conteudo.controls.extend([
                    ft.Text(
                        "Adicionar novo horário",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),

                    data,
                    hora,
                    vagas,
                    mensagem,

                    primary_button(
                        "Salvar horário",
                        salvar_horario
                    ),

                    ft.Divider(),

                    ft.Text(
                        "Horários cadastrados",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),

                    *lista_horarios
                ])

            # -------------------------
            # ABA RESERVAS
            # -------------------------
            elif aba_atual == "reservas":
                reservas = listar_reservas_completas()
                grupos = {}

                for r in reservas:
                    chave = f"{r['data']} - {r['hora']}"

                    if chave not in grupos:
                        grupos[chave] = []

                    grupos[chave].append(r["aluno_nome"])

                conteudo.controls.append(
                    ft.Text(
                        "Reservas dos alunos por horário",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    )
                )

                if grupos:
                    for horario, alunos in grupos.items():

                        lista = []

                        for nome in alunos:
                            lista.append(
                                ft.Text(f"• {nome}")
                            )

                        conteudo.controls.append(
                            ft.Card(
                                content=ft.Container(
                                    padding=15,
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                horario,
                                                size=18,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Divider(),
                                            *lista
                                        ]
                                    )
                                )
                            )
                        )
                else:
                    conteudo.controls.append(
                        ft.Text("Nenhuma reserva ainda")
                    )

            conteudo.controls.append(ft.Divider())

            conteudo.controls.append(
                primary_button(
                    "Sair",
                    lambda e: logout()
                )
            )

            page.update()

        except Exception as e:
            print("ERRO ADMIN:", e)

    atualizar()

    return ft.Container(
        content=conteudo,
        padding=20,
        expand=True
    )