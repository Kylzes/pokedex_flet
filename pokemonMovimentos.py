import flet as ft

import aiohttp

class PokemonMovimentos(ft.Container):
    def __init__(self, pokemon_id, pokemon_nome):

        self.pokemon_id = pokemon_id
        self.pokemon_nome = pokemon_nome
        self.moves_list_column = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE,
            width=420,
            expand=True,
        )

        super().__init__(
            expand=True,
            alignment=ft.alignment.center,
            padding=10,
            bgcolor="#f5f5dc",
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"Movimentos do #{self.pokemon_nome}",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.ElevatedButton(
                        text="Voltar",
                        width=100,
                        on_click=lambda e: e.page.go("/"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREY_400,
                            color=ft.Colors.BLACK,
                            alignment=ft.alignment.center,
                            text_style=ft.TextStyle(
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ),
                    ft.Container(
                        width=300,
                        expand=True,
                        border_radius=30,
                        bgcolor=ft.Colors.GREY_400,
                        content=self.moves_list_column,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    async def update_moves_info(self):
        self.moves_list_column.controls.clear()
        self.moves_list_column.controls.append(
            ft.Text("Carregando movimentos...", size=18)
        )
        self.page.update()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_id}/") as response:
                    response.raise_for_status()
                    pokemon_data = await response.json()

            moves = pokemon_data.get('moves', [])
            if not moves:
                self.moves_list_column.controls.clear()
                self.moves_list_column.controls.append(
                    ft.Text("Nenhum movimento encontrado.", size=18)
                )
            else:
                self.moves_list_column.controls.clear()
                for move_info in moves:
                    move_name = move_info['move']['name']
                    self.moves_list_column.controls.append(
                        ft.Text(
                            move_name.replace('-', ' ').title(),
                            size=16,
                            color=ft.Colors.BLACK,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD,
                        )
                    )

        except aiohttp.ClientError as e:
            self.moves_list_column.controls.clear()
            self.moves_list_column.controls.append(
                ft.Text(f"Erro ao carregar movimentos: {e}", size=16, color=ft.Colors.RED_500)
            )

        if self.page:
            self.page.update()
