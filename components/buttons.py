import flet as ft


def primary_button(texto, on_click):
    return ft.Container(
        content=ft.ElevatedButton(
            texto,
            on_click=on_click,
            width=320,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                bgcolor="#1E88E5",
                color="white",
            ),
        ),
        margin=10,
    )


def success_button(texto, on_click):
    return ft.Container(
        content=ft.ElevatedButton(
            texto,
            on_click=on_click,
            width=320,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                bgcolor="#43A047",
                color="white",
            ),
        ),
        margin=10,
    )


def danger_button(texto, on_click):
    return ft.Container(
        content=ft.ElevatedButton(
            texto,
            on_click=on_click,
            width=320,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                bgcolor="#E53935",
                color="white",
            ),
        ),
        margin=10,
    )


def small_button(texto, on_click, color="#1E88E5"):
    return ft.ElevatedButton(
        texto,
        on_click=on_click,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=color,
            color="white",
        ),
    )