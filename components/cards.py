import flet as ft
from components.buttons import small_button


def card_horario_admin(horario, on_delete):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    f"📅 {horario['data']}",
                    size=18,
                    weight="bold",
                    color="#1E88E5"
                ),
                ft.Text(
                    f"⏰ {horario['hora']}",
                    size=16
                ),
                ft.Text(
                    f"👥 Vagas: {horario['vagas']}",
                    size=14,
                    color="grey"
                ),
                ft.Row(
                    alignment="end",
                    controls=[
                        small_button(
                            "Excluir",
                            lambda e: on_delete(horario["id"]),
                            "#E53935"
                        )
                    ]
                )
            ]
        ),
        padding=15,
        border_radius=20,
        bgcolor="white",
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color="#DDDDDD"
        ),
        margin=10
    )


def card_horario_aluno(horario, on_reservar):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    f"📅 {horario['data']}",
                    size=18,
                    weight="bold",
                    color="#1E88E5"
                ),
                ft.Text(
                    f"⏰ {horario['hora']}",
                    size=16
                ),
                ft.Text(
                    f"👥 Vagas: {horario['vagas']}",
                    size=14,
                    color="grey"
                ),
                ft.Row(
                    alignment="end",
                    controls=[
                        small_button(
                            "Reservar",
                            lambda e: on_reservar(horario),
                            "#43A047"
                        )
                    ]
                )
            ]
        ),
        padding=15,
        border_radius=20,
        bgcolor="white",
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color="#DDDDDD"
        ),
        margin=10
    )


def card_reserva(reserva):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    f"Aluno: {reserva['aluno_nome']}",
                    size=16,
                    weight="bold"
                ),
                ft.Text(
                    f"Horário ID: {reserva['horario_id']}",
                    size=14,
                    color="grey"
                ),
            ]
        ),
        padding=15,
        border_radius=20,
        bgcolor="#F9F9F9",
        shadow=ft.BoxShadow(
            blur_radius=8,
            spread_radius=1,
            color="#DDDDDD"
        ),
        margin=10
    )