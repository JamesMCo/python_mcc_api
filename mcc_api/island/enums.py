from graphql import GraphQLEnumType, GraphQLEnumValue


__all__ = [
    "game_enum", "rank_enum", "rotation_enum", "server_category_enum", "trophy_category_enum"
]

game_enum = GraphQLEnumType(
    name="Game",
    description="A game.",
    values={
        "BATTLE_BOX": GraphQLEnumValue(
            value="BATTLE_BOX",
            description="Battle Box."
        ),
        "DYNABALL": GraphQLEnumValue(
            value="DYNABALL",
            description="Dynaball"
        ),
        "HOLE_IN_THE_WALL": GraphQLEnumValue(
            value="HOLE_IN_THE_WALL",
            description="Hole in the Wall."
        ),
        "PARKOUR_WARRIOR": GraphQLEnumValue(
            value="PARKOUR_WARRIOR",
            description="Parkour Warrior"
        ),
        "ROCKET_SPLEEF": GraphQLEnumValue(
            value="ROCKET_SPLEEF",
            description="Rocket Spleef"
        ),
        "SKY_BATTLE": GraphQLEnumValue(
            value="SKY_BATTLE",
            description="Sky Battle"
        ),
        "TGTTOS": GraphQLEnumValue(
            value="TGTTOS",
            description="To Get To The Other Side (TGTTOS)."
        )
    }
)

rank_enum = GraphQLEnumType(
    name="Rank",
    description="A rank.",
    values={
        "CHAMP": GraphQLEnumValue(
            value="CHAMP",
            description="The Champ rank."
        ),
        "CONTESTANT": GraphQLEnumValue(
            value="CONTESTANT",
            description="The Contestant rank."
        ),
        "CREATOR": GraphQLEnumValue(
            value="CREATOR",
            description="The Creator rank."
        ),
        "GRAND_CHAMP": GraphQLEnumValue(
            value="GRAND_CHAMP",
            description="The Grand Champ rank."
        ),
        "GRAND_CHAMP_ROYALE": GraphQLEnumValue(
            value="GRAND_CHAMP_ROYALE",
            description="The Grand Champ Royale rank."
        ),
        "MODERATOR": GraphQLEnumValue(
            value="MODERATOR",
            description="The Moderator rank."
        ),
        "NOXCREW": GraphQLEnumValue(
            value="NOXCREW",
            description="The Noxcrew rank."
        )
    }
)

rotation_enum = GraphQLEnumType(
    name="Rotation",
    description="A rotation period.\n\n"
                "Each period resets at 10AM UTC.",
    values={
        "DAILY": GraphQLEnumValue(
            value="DAILY",
            description="A daily rotation that resets."
        ),
        "WEEKLY": GraphQLEnumValue(
            value="WEEKLY",
            description="A weekly rotation that resets on Tuesdays."
        ),
        "MONTHLY": GraphQLEnumValue(
            value="MONTHLY",
            description="A monthly rotation that resets on the first day of every month."
        ),
        "YEARLY": GraphQLEnumValue(
            value="YEARLY",
            description="A yearly rotation that resets on the first day of every year."
        ),
        "LIFETIME": GraphQLEnumValue(
            value="LIFETIME",
            description="A lifetime rotation; a rotation period used to indicate something never rotates."
        )
    }
)

server_category_enum = GraphQLEnumType(
    name="ServerCategory",
    description="The category of a server.",
    values={
        "GAME": GraphQLEnumValue(
            value="GAME",
            description="A game server."
        ),
        "LIMBO": GraphQLEnumValue(
            value="LIMBO",
            description="A limbo server."
        ),
        "LOBBY": GraphQLEnumValue(
            value="LOBBY",
            description="A lobby server."
        ),
        "QUEUE": GraphQLEnumValue(
            value="QUEUE",
            description="A queue server"
        )
    }
)

trophy_category_enum = GraphQLEnumType(
    name="TrophyCategory",
    description="The categories for trophies.",
    values={
        "SKILL": GraphQLEnumValue(
            value="SKILL",
            description="Skill trophies."
        ),
        "STYLE": GraphQLEnumValue(
            value="STYLE",
            description="Style trophies."
        )
    }
)
