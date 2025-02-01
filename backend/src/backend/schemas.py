"""Schemas for the backend."""


from uuid import UUID, uuid4

from pydantic import BaseModel, PrivateAttr, computed_field


class Position(BaseModel):
    """Position class."""

    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        """Add two positions.

        Arguments:
        ---------
            other : Position
                Other position.

        Returns:
        -------
            Position: Sum of two positions.

        """
        return Position(x=self.x + other.x, y=self.y + other.y)


class Player(BaseModel):
    """Player class."""

    name: str
    position: Position
    _uuid: UUID = PrivateAttr(default_factory=uuid4)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def uuid(self) -> str:
        """Player UUID."""
        return self._uuid.hex

    def __eq__(self, other: object) -> bool:
        """Check if two players are equal.

        Arguments:
        ---------
            other : object
                Other player.

        Returns:
        -------
            bool: True if players are equal, False otherwise.

        """
        return isinstance(other, Player) and (
            # self.uuid == other.uuid or
            self.name == other.name
        )

    def __hash__(self) -> int:
        """Hash player.

        Returns
        -------
            int: Hashed player.

        """
        return hash((
            # self.uuid,
            self.name,
        ))
