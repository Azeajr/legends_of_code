"""Module contains the game engine logic."""

import logging
from typing import Any

from backend.schemas import Player, Position

logger = logging.getLogger(__name__)


class GameMap:
    """Map class."""

    # name: str = "Map"
    # size: tuple[int, int] = (10, 10)
    # players: list[Player] | None = None
    _initialized: bool = False
    __instance = None

    def __new__(cls, *_args: Any, **_kwargs: Any) -> "GameMap":
        """Singleton pattern.

        Returns
        -------
            GameMap: GameMap instance.

        """
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        name: str = "Map",
        size: tuple[int, int] = (10, 10),
        # players: list[Player] | None = None,
        players: dict[str, Player] | None = None,
    ) -> None:
        """Initialize the map.

        Arguments:
        ---------
            name : str
                Map name.
            size : tuple[int, int]
                Map size.
            players : list[Player], optional
                List of players, by default None

        """
        if not self._initialized:
            self.name = name
            self.size = size
            self.players: dict[str, Player] = players or {}
            self._initialized = True

    def add_player(self, player: Player) -> Player | None:
        """Add player to the map.

        Arguments:
        ---------
            player : Player
                Player to add.

        Returns:
        -------
            Player | None: Player if added, None otherwise.

        """
        if player not in self.players:
            self.players[player.uuid] = player
            return player
        msg = f"Player {player} already exists on the map."
        logger.error(msg)
        return None

    def remove_player(self, player: Player) -> Player | None:
        """Remove player from the map.

        Arguments:
        ---------
            player : Player
                Player to remove.

        Returns:
        -------
            Player | None: Player if removed, None otherwise.

        """
        try:
            self.players.pop(player.uuid)
        except ValueError:
            msg = f"Player {player} not found on the map."
            logger.exception(msg)
            return None
        else:
            return player

    def move_player(self, player: Player, delta: Position) -> Player | None:
        """Move player on the map.

        Arguments:
        ---------
            player : Player
                Player to move.
            delta : Position
                Position delta.

        Returns:
        -------
            Player | None: Player if moved, None otherwise

        """
        if (
            player in self.players
            and self.size[0] > player.position.x + delta.x >= 0
            and self.size[1] > player.position.y + delta.y >= 0
        ):
            # self.players[self.players.index(player)].position += delta
            self.players[player.uuid].position += delta
            return self.players[player.uuid]
        msg = f"Player {player} not found on the map."
        logger.error(msg)
        return None

    def print_map(self) -> str:
        """Print map.

        Returns
        -------
            str: Map as string.

        """
        game_map = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]
        for player in self.players:
            game_map[self.players[player].position.y][
                self.players[player].position.x
            ] += 1

        return "\n".join("".join(str(cell) for cell in row) for row in game_map)


def get_game_map() -> GameMap:
    """Get game map.

    Returns
    -------
        GameMap: Game map.

    """
    return GameMap()
