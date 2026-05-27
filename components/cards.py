import flet as ft
from components.buttons import small_button


# =========================
# CARD HORÁRIO ADMIN
# =========================

def card_horario_admin(horario, on_delete):

    return ft.Container(
        expand=True,
        margin=ft.margin.only(bottom=18),
        padding=20,
        border_radius=24,
        bgcolor="white",
        shadow=ft.BoxShadow(
            blur_radius=18,
            spread_radius=1,
            color="#E2E8F0"
        ),

        content=ft.Column(
            spacing=15,
            controls=[

                # DATA
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CALENDAR_MONTH,
                            color="#2563EB",
                            size=22
                        ),

                        ft.Text(
                            horario["data"],
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1E293B",
                            expand=True
                        )
                    ]
                ),

                # HORA
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.ACCESS_TIME,
                            color="#64748B",
                            size=20
                        ),

                        ft.Text(
                            horario["hora"],
                            size=16,
                            color="#475569"
                        )
                    ]
                ),

                # VAGAS
                ft.Container(
                    padding=10,
                    border_radius=14,
                    bgcolor="#EFF6FF",

                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.GROUPS,
                                size=20,
                                color="#2563EB"
                            ),

                            ft.Text(
                                f"{horario['vagas']} vagas disponíveis",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color="#2563EB",
                                expand=True
                            )
                        ]
                    )
                ),

                # BOTÃO
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        small_button(
                            "Excluir",
                            lambda e: on_delete(horario["id"]),
                            "#DC2626"
                        )
                    ]
                )
            ]
        )
    )


# =========================
# CARD HORÁRIO ALUNO
# =========================

def card_horario_aluno(horario, on_reservar):

    return ft.Container(
        expand=True,
        margin=ft.margin.only(bottom=18),
        padding=20,
        border_radius=24,
        bgcolor="white",

        shadow=ft.BoxShadow(
            blur_radius=18,
            spread_radius=1,
            color="#E2E8F0"
        ),

        content=ft.Column(
            spacing=15,
            controls=[

                # DATA
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CALENDAR_MONTH,
                            color="#2563EB",
                            size=22
                        ),

                        ft.Text(
                            horario["data"],
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1E293B",
                            expand=True
                        )
                    ]
                ),

                # HORA
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.ACCESS_TIME,
                            color="#64748B",
                            size=20
                        ),

                        ft.Text(
                            horario["hora"],
                            size=16,
                            color="#475569"
                        )
                    ]
                ),

                # VAGAS
                ft.Container(
                    padding=10,
                    border_radius=14,
                    bgcolor="#ECFDF5",

                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.GROUPS,
                                size=20,
                                color="#16A34A"
                            ),

                            ft.Text(
                                f"{horario['vagas']} vagas disponíveis",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color="#16A34A",
                                expand=True
                            )
                        ]
                    )
                ),

                # BOTÃO
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        small_button(
                            "Reservar",
                            lambda e: on_reservar(horario),
                            "#16A34A"
                        )
                    ]
                )
            ]
        )
    )


# =========================
# CARD RESERVA
# =========================

def card_reserva(reserva):

    return ft.Container(
        expand=True,
        margin=ft.margin.only(bottom=16),
        padding=20,
        border_radius=22,
        bgcolor="white",

        shadow=ft.BoxShadow(
            blur_radius=14,
            spread_radius=1,
            color="#E2E8F0"
        ),

        content=ft.Column(
            spacing=12,
            controls=[

                # NOME
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.PERSON,
                            color="#2563EB",
                            size=22
                        ),

                        ft.Text(
                            reserva["aluno_nome"],
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#1E293B",
                            expand=True
                        )
                    ]
                ),

                # HORÁRIO
                ft.Container(
                    padding=10,
                    border_radius=14,
                    bgcolor="#F8FAFC",

                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.EVENT,
                                size=18,
                                color="#64748B"
                            ),

                            ft.Text(
                                f"ID Horário: {reserva['horario_id']}",
                                size=14,
                                color="#475569",
                                expand=True
                            )
                        ]
                    )
                )
            ]
        )
    )