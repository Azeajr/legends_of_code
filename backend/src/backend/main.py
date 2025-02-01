"""Main module for the backend."""

from fastapi import FastAPI

from backend.routers import maps, players

app = FastAPI()

app.include_router(players.router)
app.include_router(maps.router)
# game_map = GameMap(name="Map", size=(10, 10))
# game_map.add_player(Player(name="Player1", position=(0, 0)))


# @app.get("/map")
# def read_map() -> str:
#     """Read map endpoint.

#     Returns
#     -------
#         str: Map as string.

#     """
#     return game_map.print_map()

# @app.put("/player/{player_name}")
# def add_player(player_name: str) -> str:
#     """Add player endpoint.

#     Parameters
#     ----------
#         player_name : str
#             Player name.

#     Returns
#     -------
#         str: Player name.

#     """
#     game_map.add_player(Player(name=player_name, position=(0, 0)))
#     return player_name
