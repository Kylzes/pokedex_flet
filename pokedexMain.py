
import flet as ft
import aiohttp

from .pokemonTypes import PokemonTypes
from .pokemonStats import PokemonStats
from .pokemonControl import PokedexControls
from .pokemonMovimentos import PokemonMovimentos

from pokedex.src.const.util import POKEMON_TYPE_COLORS

class PokedexMain(ft.Container):
    def __init__(self, on_move_click):
        self.ref_bgcolor_image = ft.Ref[ft.Container]()
        self.ref_image = ft.Ref[ft.Image]()
        self.ref_nome = ft.Ref[ft.Text]()
        self.ref_id = ft.Ref[ft.Text]()
        self.pokemon_types = PokemonTypes()
        self.pokemon_stats = PokemonStats()

        self.pokedex_controls = PokedexControls(
            on_search=self.btn_search_click,
            on_move_click=on_move_click
        )
        self.all_pokemon_names: dict = {}     #Dicionario que armazena o id e o nome

        self.current_pokemon_id = 1
        self.is_gif = False

        super().__init__(
            bgcolor="#f5f5dc",
            expand=True,
            border_radius=20,
            padding=5,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Container(
                        ref=self.ref_bgcolor_image,
                        height=300,
                        width=420,
                        border_radius=20,
                        content=ft.Stack(
                            controls=[
                                self.get_image(),
                                self.get_nome_id(),
                                self.get_btn_navegacao(ft.Icons.ARROW_BACK, left=50, on_click=self.btn_back),
                                self.get_btn_navegacao(ft.Icons.ARROW_FORWARD, right=50, on_click=self.btn_forward),
                                self.get_btn_image_gif(),
                            ]
                        )
                    ),
                    self.pokemon_types,
                    self.pokemon_stats,
                    self.pokedex_controls,
                ]
            )
        )

    def get_moves_page(self):
        return PokemonMovimentos(self.current_pokemon_id, self.get_nome().value)

    # Carre os nomes e o id para o dicionario
    async def load_all_pokemon_names(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://pokeapi.co/api/v2/pokemon?limit=1025") as response:
                    response.raise_for_status()
                    data = await response.json()

                    for i, pokemon in enumerate(data['results'], 1):
                        self.all_pokemon_names[pokemon['name']] = i
        except aiohttp.ClientError as e:
            print(f"Erro ao carregar a lista de Pokémon: {e}")

    # --- Métodos de Lógica ---
    async def update_pokemon_info(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://pokeapi.co/api/v2/pokemon/{self.current_pokemon_id}/") as response:
                    response.raise_for_status()
                    pokemon_data = await response.json()

            self.update_troca_img_gif(pokemon_data)
            self.pokemon_types.update_types(pokemon_data['types'])
            self.pokemon_stats.update_stats(pokemon_data['stats'])

            if self.page:
                self.page.update()

        except aiohttp.ClientError as e:
            print(f"Erro ao buscar Pokémon: {e}")
            self.ref_image.current.src = ""
            self.ref_nome.current.value = "Erro!"
            self.ref_id.current.value = "###"
            self.ref_bgcolor_image.current.bgcolor = ft.Colors.RED_900
            if self.page:
                self.page.update()

    def update_troca_img_gif(self, pokemon_data: dict):
        if self.is_gif:
            gif_sprite_url = pokemon_data['sprites']['other']['showdown'].get('front_default')
            if gif_sprite_url:
                self.ref_image.current.src = gif_sprite_url
                self.ref_image.current.scale = 2.0
            else:
                self.is_gif = False
                dream_world_sprite = pokemon_data['sprites']['other'].get('dream_world', {}).get('front_default')
                self.ref_image.current.src = dream_world_sprite if dream_world_sprite else pokemon_data['sprites']['front_default']
                self.ref_image.current.scale = 0.7
        else:
            dream_world_sprite = pokemon_data['sprites']['other'].get('dream_world', {}).get('front_default')
            self.ref_image.current.src = dream_world_sprite if dream_world_sprite else pokemon_data['sprites']['front_default']
            self.ref_image.current.scale = 0.7

        self.ref_id.current.value = f"#{pokemon_data['id']:03d}"
        pokemon_type_name = pokemon_data['types'][0]['type']['name']
        self.ref_bgcolor_image.current.bgcolor = POKEMON_TYPE_COLORS.get(pokemon_type_name, POKEMON_TYPE_COLORS.get('normal'))
        self.ref_nome.current.value = pokemon_data['name'].capitalize()

    def get_image(self):
        return ft.Image(ref=self.ref_image, top=0, bottom=0, left=0, right=0 ,)

    def get_nome_id(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.get_id(), self.get_nome()],
            top=0, bottom=None, left=0, right=0,
        )

    def get_nome(self):
        return ft.Text(ref=self.ref_nome, value="Bulbasaur", size=18, weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE)

    def get_id(self):
        return ft.Text(ref=self.ref_id, value="#001", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)

    def get_btn_navegacao(self, icon, top=25, bottom=None, left=None, right=None, on_click=None):
        return ft.IconButton(
            on_click=on_click, icon=icon, icon_color=ft.Colors.WHITE, icon_size=18,
            bgcolor=ft.Colors.BLACK54, top=top, bottom=bottom, left=left, right=right,
        )

    def get_btn_image_gif(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    tooltip="Imagem ou GIF",
                    icon=ft.Icons.GIF_OUTLINED, icon_color=ft.Colors.WHITE, icon_size=22,
                    bgcolor=ft.Colors.BLACK54, height=30, width=30, padding=0,
                    on_click=self.btn_troca_imagem_click
                ),
            ],
            top=None, bottom=3, left=0, right=0,
        )

    async def btn_forward(self, e):
        self.current_pokemon_id = 1 if self.current_pokemon_id >= 1025 else self.current_pokemon_id + 1
        await self.update_pokemon_info()

    async def btn_back(self, e):
        self.current_pokemon_id = 1025 if self.current_pokemon_id <= 1 else self.current_pokemon_id - 1
        await self.update_pokemon_info()

    async def btn_troca_imagem_click(self, e):
        self.is_gif = not self.is_gif
        await self.update_pokemon_info()

    async def btn_search_click(self, e):
        # Lógica de pesquisa
        nome = self.pokedex_controls.ref_search_field.current.value.lower()

        # Verifica se o textField e um número (ID)
        if nome.isdigit():
            id = int(nome)
            if 1 <= id <= 493:
                self.current_pokemon_id = id
                await self.update_pokemon_info()
                return

        # Verifica se o textField e uma string
        id = self.all_pokemon_names.get(nome)
        if id:
            self.current_pokemon_id = id
            await self.update_pokemon_info()

        # Caso não exista o pokemon
        else:
            #print(f"Pokémon '{nome}' não encontrado.")
            self.pokedex_controls.ref_search_field.current.value = "Nao encontrado!"
            self.page.update()

    def on_move_click_hander(self, e):
        e.page.go(f"/movimentos/{self.current_pokemon_id}")
