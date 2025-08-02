
import flet as ft

from pokedex.src.const.util import POKEMON_STATS_NAME


class PokemonStats(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=5,
            expand=True,
        )

    def update_stats(self, stats_data: list):
        self.controls.clear()
        for stats in stats_data:
            nome = stats['stat']['name']
            base_stat = stats['base_stat']

            numero_caixas_azuis = round((base_stat / 255) * 15)

            barra_progresso = []
            for i in range(15):
                barra_progresso.append(
                    ft.Container(
                        width=15,
                        height=30,
                        border_radius=20,
                        bgcolor=ft.Colors.BLUE_ACCENT_200 if i < numero_caixas_azuis else ft.Colors.WHITE,
                    )
                )

            self.controls.append(
                ft.Container(
                    padding=2,
                    bgcolor=ft.Colors.GREY_400,
                    border_radius=5,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                width=75,
                                value=POKEMON_STATS_NAME.get(nome, nome).upper(),
                                color=ft.Colors.BLACK,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Row(
                                expand=True,
                                spacing=5,
                                controls=barra_progresso,
                            ),
                        ]
                    )
                )
            )