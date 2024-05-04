from enum import auto, Enum
import typing as t


class UpperStrEnum(Enum):
    """Custom Enum class that acts like :class:`enum.StrEnum`, using uppercase strings."""
    def __str__(self):
        """Return the member value when asked for the string version of the member.

        As these enums use auto(), they use _generate_next_value_ and are thus guaranteed to be uppercase.
        """
        return self.value

    @staticmethod
    def _generate_next_value_(name: str, start: t.Optional[int], count: int, last_values: list[str]):
        """As with :class:`enum.StrEnum`, return the member name. However, return it as its uppercase version."""
        return name.upper()


class Game(UpperStrEnum):
    """Game identifiers accepted and returned by the MCC API."""

    MG_ROCKET_SPLEEF = auto()
    MG_SURVIVAL_GAMES = auto()
    MG_PARKOUR_WARRIOR = auto()
    MG_ACE_RACE = auto()
    MG_BINGO_BUT_FAST = auto()
    MG_TGTTOSAWAF = auto()
    MG_SKYBLOCKLE = auto()
    MG_SKY_BATTLE = auto()
    MG_HOLE_IN_THE_WALL = auto()
    MG_BATTLE_BOX = auto()
    MG_BUILD_MART = auto()
    MG_SANDS_OF_TIME = auto()
    MG_DODGEBOLT = auto()
    MG_PARKOUR_TAG = auto()
    MG_GRID_RUNNERS = auto()
    MG_MELTDOWN = auto()
    GLOBAL_STATISTICS = auto()
    LEGACY_STATISTICS = auto()
    MG_LOCKOUT_BINGO = auto()
    MG_FOOT_RACE = auto()
    MG_ROCKET_SPLEEF_OLD = auto()
    MG_RAILROAD_RUSH = auto()


class Team(UpperStrEnum):
    """Team identifiers accepted and returned by the MCC API."""

    RED = auto()
    ORANGE = auto()
    YELLOW = auto()
    LIME = auto()
    GREEN = auto()
    CYAN = auto()
    AQUA = auto()
    BLUE = auto()
    PURPLE = auto()
    PINK = auto()
    SPECTATORS = auto()
    NONE = auto()
