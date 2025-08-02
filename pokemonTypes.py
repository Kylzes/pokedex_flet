
import flet as ft

from pokedex.src.const.util import POKEMON_TYPE_COLORS

class PokemonTypes(ft.Row):
    def __init__(self):
        super().__init__(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

    def update_types(self, types_data: list):
        self.controls.clear()
        for type_data in types_data:
            type_name = type_data['type']['name']
            self.controls.append(
                ft.Container(
                    bgcolor=POKEMON_TYPE_COLORS.get(type_name),
                    width=100,
                    height=30,
                    border_radius=20,
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        value=type_name.capitalize(),
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    )
                )
            )
