from graphql import GraphQLEnumType, GraphQLEnumValue


__all__ = [
    "cosmetic_category_enum",
    "fish_catch_time_enum",
    "fish_weight_enum",
    "game_enum",
    "rank_enum",
    "rarity_enum",
    "rotation_enum",
    "server_category_enum",
    "trophy_category_enum"
]

cosmetic_category_enum = GraphQLEnumType(
    name="CosmeticCategory",
    description="Different categories of cosmetics.",
    values={
        "ACCESSORY": GraphQLEnumValue(
            value="ACCESSORY",
            description="Accessories."
        ),
        "AURA": GraphQLEnumValue(
            value="AURA",
            description="Auras."
        ),
        "CLOAK": GraphQLEnumValue(
            value="CLOAK",
            description="Cloaks."
        ),
        "HAIR": GraphQLEnumValue(
            value="HAIR",
            description="Hair."
        ),
        "HAT": GraphQLEnumValue(
            value="HAT",
            description="Hats."
        ),
        "ROD": GraphQLEnumValue(
            value="ROD",
            description="Fishing rods."
        ),
        "TRAIL": GraphQLEnumValue(
            value="TRAIL",
            description="Trails."
        )
    }
)

fish_catch_time_enum = GraphQLEnumType(
    name="FishCatchTime",
    description="The time a fish can be caught in.",
    values={
        "ALWAYS": GraphQLEnumValue(
            value="ALWAYS",
            description="The fish can always be caught."
        ),
        "DAY": GraphQLEnumValue(
            value="DAY",
            description="The fish can only be caught during daytime."
        ),
        "NIGHT": GraphQLEnumValue(
            value="NIGHT",
            description="The fish can only be caught during nighttime."
        )
    }
)

fish_weight_enum = GraphQLEnumType(
    name="FishWeight",
    description="The weight of a fish.\n\n"
                "Note that some weights are not used for crabs, or are only used for crabs.",
    values={
        "AVERAGE": GraphQLEnumValue(
            value="AVERAGE",
            description="Average."
        ),
        "COLOSSAL": GraphQLEnumValue(
            value="COLOSSAL",
            description="Colossal.\n\n"
                        "This weight is only used for crabs."
        ),
        "GARGANTUAN": GraphQLEnumValue(
            value="GARGANTUAN",
            description="Gargantuan.\n\n"
                        "This weight is not used for crabs."
        ),
        "LARGE": GraphQLEnumValue(
            value="LARGE",
            description="Large."
        ),
        "MASSIVE": GraphQLEnumValue(
            value="MASSIVE",
            description="Massive.\n\n"
                        "This weight is not used for crabs."
        )
    }
)

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
            description="Dynaball."
        ),
        "HOLE_IN_THE_WALL": GraphQLEnumValue(
            value="HOLE_IN_THE_WALL",
            description="Hole in the Wall."
        ),
        "PARKOUR_WARRIOR": GraphQLEnumValue(
            value="PARKOUR_WARRIOR",
            description="Parkour Warrior."
        ),
        "ROCKET_SPLEEF": GraphQLEnumValue(
            value="ROCKET_SPLEEF",
            description="Rocket Spleef."
        ),
        "SKY_BATTLE": GraphQLEnumValue(
            value="SKY_BATTLE",
            description="Sky Battle."
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

rarity_enum = GraphQLEnumType(
    name="Rarity",
    description="Different tiers of rarity.",
    values={
        "COMMON": GraphQLEnumValue(
            value="COMMON",
            description="Common."
        ),
        "EPIC": GraphQLEnumValue(
            value="EPIC",
            description="Epic."
        ),
        "LEGENDARY": GraphQLEnumValue(
            value="LEGENDARY",
            description="Legendary."
        ),
        "MYTHIC": GraphQLEnumValue(
            value="MYTHIC",
            description="Mythic."
        ),
        "RARE": GraphQLEnumValue(
            value="RARE",
            description="Rare."
        ),
        "UNCOMMON": GraphQLEnumValue(
            value="UNCOMMON",
            description="Uncommon."
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
        "ANGLER": GraphQLEnumValue(
            value="ANGLER",
            description="Angler trophies."
        ),
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
