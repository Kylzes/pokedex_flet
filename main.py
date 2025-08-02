
import flet as ft
import re

from inicial.pokedexMain import PokedexMain


async def main(page: ft.Page):
    page.title = "Pokedex"
    page.window.height = 720
    page.window.width = 420
    page.window.resizable = False
    page.window.maximizable = False
    page.padding = 0

    pokedex_main_view = PokedexMain(
        on_move_click=lambda e: e.page.go(f"/movimentos/{pokedex_main_view.current_pokemon_id}")
    )

    async def route_change(e):
        page.clean()

        if e.route.startswith("/movimentos/"):
            match = re.match(r"/movimentos/(\d+)", e.route)
            if match:
                pokemon_id = int(match.group(1))

                #cria a página de movimentos
                movies_view = pokedex_main_view.get_moves_page()
                page.add(movies_view)

                # Chama a função de atualização para carregar os dados
                await movies_view.update_moves_info()
            else:
                page.go("/")
        else:
            page.add(pokedex_main_view)
            await pokedex_main_view.update_pokemon_info()

    page.on_route_change = route_change
    await pokedex_main_view.load_all_pokemon_names()
    page.go("/")


ft.app(main)
