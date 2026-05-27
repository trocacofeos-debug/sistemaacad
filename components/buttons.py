import flet as ft


# =========================
# BOTÃO PRINCIPAL
# =========================

def primary_button(texto, on_click):

    return ft.Container(
        width=float("inf"),
        margin=ft.margin.only(top=5, bottom=5),

        content=ft.ElevatedButton(
            text=texto,
            on_click=on_click,
            width=float("inf"),
            height=55,

            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor="#2563EB",
                color="white",

                text_style=ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                elevation=3
            )
        )
    )


# =========================
# BOTÃO SUCESSO
# =========================

def success_button(texto, on_click):

    return ft.Container(
        width=float("inf"),
        margin=ft.margin.only(top=5, bottom=5),

        content=ft.ElevatedButton(
            text=texto,
            on_click=on_click,
            width=float("inf"),
            height=55,

            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor="#16A34A",
                color="white",

                text_style=ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                elevation=3
            )
        )
    )


# =========================
# BOTÃO PERIGO
# =========================

def danger_button(texto, on_click):

    return ft.Container(
        width=float("inf"),
        margin=ft.margin.only(top=5, bottom=5),

        content=ft.ElevatedButton(
            text=texto,
            on_click=on_click,
            width=float("inf"),
            height=55,

            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor="#DC2626",
                color="white",

                text_style=ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

                elevation=3
            )
        )
    )


# =========================
# BOTÃO PEQUENO
# =========================

def small_button(texto, on_click, color="#2563EB"):

    return ft.ElevatedButton(
        text=texto,
        on_click=on_click,
        height=42,

        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=14),
            bgcolor=color,
            color="white",

            text_style=ft.TextStyle(
                size=14,
                weight=ft.FontWeight.W_600
            )
        )
    )