"""Maps router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from backend.game_eng import GameMap, get_game_map

router = APIRouter(
    prefix="/maps",
    tags=["maps"],
)


@router.get("/print_map/")
def print_map(
    game_map: Annotated[GameMap, Depends(get_game_map)],
) -> dict[str, str]:
    """Print map endpoint.

    Returns
    -------
        dict: Map.

    """
    return {
        "map": game_map.print_map(),
    }
