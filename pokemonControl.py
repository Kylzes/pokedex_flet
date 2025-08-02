import flet as ft


class PokedexControls(ft.Row):
    def __init__(self, on_search, on_move_click):

        self.ref_search_field = ft.Ref[ft.TextField]()

        super().__init__(
            spacing=5,
            height=50,
            expand_loose=True,
            controls=[
                self.btn_movimentos(on_move_click),
                self.get_text_field(on_search),
            ]
        )

    def get_text_field(self, on_search):
        return ft.TextField(
            ref=self.ref_search_field,
            width=200,
            hint_text="Pokemon",
            text_align=ft.TextAlign.LEFT,
            suffix=ft.IconButton(
                icon=ft.Icons.SEARCH,
                icon_color=ft.Colors.GREY_600,
                on_click=on_search  # Chama a função de pesquisa
            ),
            border_color=ft.Colors.BLACK,
            text_style=ft.TextStyle(
                size=15,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            )
        )

    def btn_movimentos(self, on_move_click):
        return ft.TextButton(
            on_click=on_move_click,
            width=100,
            text="Mov",
            tooltip="Movimentos",
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREY_400,
                color=ft.Colors.BLACK,
                text_style=ft.TextStyle(
                    size=20,
                    weight=ft.FontWeight.BOLD,
                )
            ),
        )
