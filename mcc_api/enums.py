from enum import StrEnum


class Game(StrEnum):
    """Game identifiers accepted and returned by the MCC API."""

    MG_ROCKET_SPLEEF = "MG_ROCKET_SPLEEF"
    MG_SURVIVAL_GAMES = "MG_SURVIVAL_GAMES"
    MG_PARKOUR_WARRIOR = "MG_PARKOUR_WARRIOR"
    MG_ACE_RACE = "MG_ACE_RACE"
    MG_BINGO_BUT_FAST = "MG_BINGO_BUT_FAST"
    MG_TGTTOSAWAF = "MG_TGTTOSAWAF"
    MG_SKYBLOCKLE = "MG_SKYBLOCKLE"
    MG_SKY_BATTLE = "MG_SKY_BATTLE"
    MG_HOLE_IN_THE_WALL = "MG_HOLE_IN_THE_WALL"
    MG_BATTLE_BOX = "MG_BATTLE_BOX"
    MG_BUILD_MART = "MG_BUILD_MART"
    MG_SANDS_OF_TIME = "MG_SANDS_OF_TIME"
    MG_DODGEBOLT = "MG_DODGEBOLT"
    MG_PARKOUR_TAG = "MG_PARKOUR_TAG"
    MG_GRID_RUNNERS = "MG_GRID_RUNNERS"
    MG_MELTDOWN = "MG_MELTDOWN"
    GLOBAL_STATISTICS = "GLOBAL_STATISTICS"
    LEGACY_STATISTICS = "LEGACY_STATISTICS"
    MG_LOCKOUT_BINGO = "MG_LOCKOUT_BINGO"
    MG_FOOT_RACE = "MG_FOOT_RACE"
    MG_ROCKET_SPLEEF_OLD = "MG_ROCKET_SPLEEF_OLD"


class Team(StrEnum):
    """Team identifiers accepted and returned by the MCC API."""

    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    LIME = "LIME"
    GREEN = "GREEN"
    CYAN = "CYAN"
    AQUA = "AQUA"
    BLUE = "BLUE"
    PURPLE = "PURPLE"
    PINK = "PINK"
    SPECTATORS = "SPECTATORS"
    NONE = "NONE"