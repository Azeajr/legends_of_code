"""Players router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from backend.game_eng import GameMap, get_game_map
from backend.schemas import Player, Position

router = APIRouter(
    prefix="/players",
    tags=["players"],
)


@router.get("/")
def get_players(
    game_map: Annotated[GameMap, Depends(get_game_map)],
) -> dict[str, dict[str, Player]]:
    """Read players endpoint.

    Returns
    -------
        dict: Players.

    """
    return {
        "players": game_map.players,
        # [player.name for player in game_map.players],
    }


@router.post("/add_player/")
def add_player(
    player: Player,
    game_map: Annotated[GameMap, Depends(get_game_map)],
) -> Player:
    """Add player endpoint.

    Returns
    -------
        player: Player name.

    Raises
    ------
        HTTPException: Player already exists.

    """
    if game_map.add_player(player):
        return player
    raise HTTPException(status_code=400, detail="Player already exists.")


@router.post("/remove_player/")
def remove_player(
    player: Player,
    game_map: Annotated[GameMap, Depends(get_game_map)],
) -> Player:
    """Remove player endpoint.

    Returns
    -------
        Player: Removed player.

    Raises
    ------
        HTTPException: Player does not exist.

    """
    if game_map.remove_player(player):
        return player
    raise HTTPException(status_code=400, detail="Player does not exist.")


@router.post("/move_player/")
def move_player(
    player: Player,
    delta: Position,
    # move_player_request: MovePlayerRequest,
    game_map: Annotated[GameMap, Depends(get_game_map)],
) -> Player:
    """Move player endpoint.

    Returns
    -------
        Player: Moved player.

    Raises
    ------
        HTTPException: Player does not exist.

    """
    moved_player = game_map.move_player(player, delta)
    if moved_player:
        return moved_player
    raise HTTPException(status_code=400, detail="Player does not exist.")
