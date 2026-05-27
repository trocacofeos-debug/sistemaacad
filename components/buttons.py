import flet as ft


# =========================
# BOTÃO PRINCIPAL
# =========================

def primary_button(texto, on_click):

    return ft.Container(
        width=float("inf"),
        margin=5,

        content=ft.ElevatedButton(
            content=ft.Text(
                texto,
                size=16,
                weight=ft.FontWeight.BOLD,
                color="white"
            ),

            on_click=on_click,
            width=float("inf"),
            height=55,

            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor="#2563EB",
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
        margin=5,

        content=ft.ElevatedButton(
            content=ft.Text(
                texto,
                size=16,
                weight=ft.FontWeight.BOLD,
                color="white"
            ),

            on_click=on_click,
            width=float("inf"),
            height=55,

            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor="#16A34A",
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
        margin=5,

        content=ft.ElevatedButton(
            content=ft.Text(
                texto,
                size=16,
                weight=ft.FontWeight.BOLD,
                color="white"
            ),

            on_click=on_click,
            width=float("inf"),
            height=55,

            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor="#DC2626",
                elevation=3
            )
        )
    )


# =========================
# BOTÃO PEQUENO
# =========================

def small_button(texto, on_click, color="#2563EB"):

    return ft.ElevatedButton(
        content=ft.Text(
            texto,
            size=14,
            weight=ft.FontWeight.W_600,
            color="white"
        ),

        on_click=on_click,
        height=42,

        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=14),
            bgcolor=color
        )
    )