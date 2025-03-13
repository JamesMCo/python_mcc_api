from .enums import *
from .scalars import *
from graphql import (
    GraphQLArgument, GraphQLBoolean, GraphQLField, GraphQLInputField, GraphQLInputObjectType,
    GraphQLInt, GraphQLList, GraphQLNonNull, GraphQLObjectType, GraphQLString
)


__all__ = [
    "collections_type",
    "cosmetic_type",
    "cosmetic_ownership_state_type",
    "crown_level_type",
    "currency_type",
    "fish_type",
    "fish_caught_weight_type",
    "fish_record_type",
    "leaderboard_entry_type",
    "level_data_type",
    "mcc_plus_status_type",
    "party_type",
    "player_type",
    "progression_data_type",
    "query_type",
    "server_type",
    "social_type",
    "statistic_type",
    "statistic_value_result_type",
    "statistics_type",
    "status_type",
    "spectaqloption_type",
    "trophy_data_type"
]

from .scalars import date_scalar

collections_type = GraphQLObjectType(
    name="Collections",
    description="Collections data.",
    fields=lambda: {
        "cosmetics": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(cosmetic_ownership_state_type))),
            description="Returns the ownership state of all cosmetics, optionally in a category and/or collection.",
            args={
                "category": GraphQLArgument(
                    cosmetic_category_enum,
                    default_value=None
                ),
                "collection": GraphQLArgument(
                    GraphQLString,
                    default_value=None
                )
            }
        ),
        "currency": GraphQLField(
            GraphQLNonNull(currency_type),
            description="The player's earned currency."
        ),
        "equippedCosmetics": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(cosmetic_type))),
            description="A list of cosmetics the player currently has equipped."
        ),
        "fish": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(fish_record_type))),
            description="Returns the record data for all fish, optionally in a specific collection.",
            args={
                "collection": GraphQLArgument(
                    GraphQLString,
                    default_value=None
                )
            }
        )
    }
)

cosmetic_type = GraphQLObjectType(
    name="Cosmetic",
    description="A cosmetic.",
    fields={
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of the cosmetic."
        ),
        "canBeDonated": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="If this cosmetic can be donated for Royal Reputation."
        ),
        "category": GraphQLField(
            GraphQLNonNull(cosmetic_category_enum),
            description="The category the cosmetic is in."
        ),
        "collection": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The collection this cosmetic is in."
        ),
        "colorable": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="If this cosmetic can be colored using Chroma Packs."
        ),
        "description": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The description of the cosmetic."
        ),
        "globalNumberOwned": GraphQLField(
            GraphQLString,
            description="The number of people who own this cosmetic.\n\n"
                        "The exact number is only displayed if fewer than 1000 players own this cosmetic.\n"
                        "Otherwise, either `1000+` or `10000+` will be returned, indicating the real value is higher "
                        "than this number.\n"
                        "Some cosmetics are excluded from ownership reporting, for these cosmetics `null` will be "
                        "returned."
        ),
        "isBonusTrophies": GraphQLField(
            GraphQLBoolean,
            description="If this cosmetic awards bonus trophies.\n\n"
                        "This will be `null` if the cosmetic does not award any trophies."
        ),
        "rarity": GraphQLField(
            GraphQLNonNull(rarity_enum),
            description="The rarity of the cosmetic."
        ),
        "trophies": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of trophies this cosmetic awards.\n\n"
                        "Note that this does not include the completion bonus for applying all "
                        "Chroma Packs to the cosmetic."
        )
    }
)

cosmetic_ownership_state_type = GraphQLObjectType(
    name="CosmeticOwnershipState",
    description="The ownership state of a cosmetic.",
    fields={
        "chromaPacks": GraphQLField(
            GraphQLList(GraphQLNonNull(GraphQLString)),
            description="The Chroma Packs that have applied to this cosmetic, if it is colorable."
        ),
        "cosmetic": GraphQLField(
            GraphQLNonNull(cosmetic_type),
            description="The cosmetic in question."
        ),
        "donationsMade": GraphQLField(
            GraphQLInt,
            description="The number of Royal Reputation donations that have been made of this cosmetic, "
                        "if it can be donated."
        ),
        "owned": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="If the cosmetic is owned."
        )
    }
)

crown_level_type = GraphQLObjectType(
    name="CrownLevel",
    description="A Crown Level and associated trophy data.",
    fields=lambda: {
        "fishingLevelData": GraphQLField(
            GraphQLNonNull(level_data_type),
            description="The fishing level data."
        ),
        "levelData": GraphQLField(
            GraphQLNonNull(level_data_type),
            description="The overall level data."
        ),
        "trophies": GraphQLField(
            GraphQLNonNull(trophy_data_type),
            description="The amount of trophies the player has.",
            args={
                "category": GraphQLArgument(
                    trophy_category_enum,
                    default_value=None
                )
            }
        )
    }
)

currency_type = GraphQLObjectType(
    name="Currency",
    description="A player's earned currency.",
    fields={
        "anglrTokens": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of A.N.G.L.R. Tokens the player currently has."
        ),
        "coins": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of coins the player currently has."
        ),
        "materialDust": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of material dust the player currently has."
        ),
        "royalReputation": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of Royal Reputation the player currently has."
        ),
        "silver": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of silver the player currently has."
        )
    }
)

fish_type = GraphQLObjectType(
    name="Fish",
    description="A fish.\n\n"
                "Queries on this type that accept a weight as an argument will return `null` if this fish does not "
                "support the provided weight.",
    fields={
        "catchTime": GraphQLField(
            GraphQLNonNull(fish_catch_time_enum),
            description="The time this fish can be caught."
        ),
        "climate": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The climate this fish can be found in."
        ),
        "collection": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The collection this fish can be found in."
        ),
        "elusive": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="If this fish is elusive."
        ),
        "globalNumberCaught": GraphQLField(
            GraphQLString,
            description="The number of people who have caught this fish.\n\n"
                        "The exact number is only displayed if fewer than 1000 players have caught this fish.\n"
                        "Otherwise, either `1000+` or `10000+` will be returned, indicating the real value is higher "
                        "than this number.",
            args={
                "weight": GraphQLArgument(
                    GraphQLNonNull(fish_weight_enum)
                )
            }
        ),
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of the fish."
        ),
        "rarity": GraphQLField(
            GraphQLNonNull(rarity_enum),
            description="The rarity of the fish."
        ),
        "trophies": GraphQLField(
            GraphQLInt,
            description="The number of trophies awarded for catching this fish in a given weight.",
            args={
                "weight": GraphQLArgument(
                    GraphQLNonNull(fish_weight_enum)
                )
            }
        ),
        "sellingPrice": GraphQLField(
            GraphQLInt,
            description="The number of A.N.G.L.R. Tokens given for selling this fish in a given weight.",
            args={
                "weight": GraphQLArgument(
                    GraphQLNonNull(fish_weight_enum)
                )
            }
        )
    }
)

fish_caught_weight_type = GraphQLObjectType(
    name="FishCaughtWeight",
    description="Data about a caught fish weight.",
    fields={
        "firstCaught": GraphQLField(
            GraphQLNonNull(date_scalar),
            description="When the player first caught this weight."
        ),
        "weight": GraphQLField(
            GraphQLNonNull(fish_weight_enum),
            description="The weight that was caught."
        )
    }
)

fish_record_type = GraphQLObjectType(
    name="FishRecord",
    description="A record of the weight of fish that have been caught.",
    fields={
        "fish": GraphQLField(
            GraphQLNonNull(fish_type),
            description="The fish this record is for."
        ),
        "weights": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(fish_caught_weight_type))),
            description="A list of data about the weights that have been caught."
        )
    }
)

leaderboard_entry_type = GraphQLObjectType(
    name="LeaderboardEntry",
    description="An entry in a leaderboard.",
    fields=lambda: {
        "player": GraphQLField(
            player_type,
            description="The player who has this entry.\n\n"
                        "This will be `null` if the player does not have the statistics enabled for the API.\n"
                        "However, for Crown Level or Trophy count leaderboards, the player will not be `null`."
        ),
        "rank": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The rank for this entry."
        ),
        "value": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The value for this entry."
        )
    }
)

level_data_type = GraphQLObjectType(
    name="LevelData",
    description="Data relating to a level.",
    fields=lambda: {
        "evolution": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The zero-indexed evolution of the level.",
        ),
        "level": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The overall level."
        ),
        "nextEvolutionLevel": GraphQLField(
            GraphQLInt,
            description="The next level that will have an evolution, if any."
        ),
        "nextLevelProgress": GraphQLField(
            progression_data_type,
            description="The progress the player is making towards their next level, if any."
        )
    }
)

mcc_plus_status_type = GraphQLObjectType(
    name="MCCPlusStatus",
    description="The status of a player's MCC+ subscription.",
    fields={
        "evolution": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The current evolution index for MCC+ icon."
        ),
        "streakStart": GraphQLField(
            GraphQLNonNull(datetime_scalar),
            description="The instant they started their current streak."
        ),
        "totalDays": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The total number of days they have been subscribed for."
        )
    }
)

party_type = GraphQLObjectType(
    name="Party",
    description="A player's status within a party.",
    fields=lambda: {
        "active": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="Whether the player is in an active party."
        ),
        "leader": GraphQLField(
            player_type,
            description="The leader of the party, populated if the party exists."
        ),
        "members": GraphQLField(
            GraphQLList(GraphQLNonNull(player_type)),
            description="The members of the party, populated if the party exists."
        )
    }
)

player_type = GraphQLObjectType(
    name="Player",
    description="A player who has logged in to MCC Island.",
    fields=lambda: {
        "collections": GraphQLField(
            collections_type,
            description="Collections data for the player.\n\n"
                        "This method is conditional on the player having the in-game "
                        "\"collections\" API setting enabled."
        ),
        "crownLevel": GraphQLField(
            GraphQLNonNull(crown_level_type),
            description="The player's Crown Level and associated trophy data."
        ),
        "mccPlusStatus": GraphQLField(
            mcc_plus_status_type,
            description="The player's MCC+ status, if currently subscribed."
        ),
        "ranks": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(rank_enum))),
            description="The ranks which the user is associated with, if any."
        ),
        "social": GraphQLField(
            social_type,
            description="Social data for the player.\n\n"
                        "This method is conditional on the player having the in-game "
                        "\"social\" API setting enabled."
        ),
        "statistics": GraphQLField(
            statistics_type,
            description="Statistics data for the player.\n\n"
                        "This method is conditional on the player having the in-game "
                        "\"statistics\" API setting enabled."
        ),
        "status": GraphQLField(
            status_type,
            description="The current status of the player.\n\n"
                        "This method is conditional on the player having the in-game "
                        "\"status\" API setting enabled."
        ),
        "username": GraphQLField(
            GraphQLString,
            description="The player's username, if known."
        ),
        "uuid": GraphQLField(
            GraphQLNonNull(uuid_scalar),
            description="The player's Minecraft UUID in dashed format."
        )
    }
)

progression_data_type = GraphQLObjectType(
    name="ProgressionData",
    description="Data for types that track some form of progression.",
    fields={
        "obtained": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount obtained."
        ),
        "obtainable": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount that can be obtained."
        )
    }
)

query_type = GraphQLObjectType(
    name="Query",
    description="Available queries.",
    fields=lambda: {
        "player": GraphQLField(
            player_type,
            description="Given a UUID, returns a Player if they have logged in to MCC Island.",
            args={
                "uuid": GraphQLArgument(
                    GraphQLNonNull(uuid_scalar)
                )
            }
        ),
        "playerByUsername": GraphQLField(
            player_type,
            description="Given a username, returns a Player object if they have logged into "
                        "MCC Island with this username.\n\n"
                        "This method may not return a player that has this username if they "
                        "have not logged in recently enough for us\n"
                        "to verify that the player still owns this username.",
            args={
                "username": GraphQLArgument(
                    GraphQLNonNull(GraphQLString)
                )
            }
        ),
        "statistics": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(statistic_type))),
            description="Returns a list of all known statistics."
        ),
        "statistic": GraphQLField(
            statistic_type,
            description="Returns a statistic by it's name.",
            args={
                "key": GraphQLArgument(
                    GraphQLNonNull(GraphQLString)
                )
            }
        ),
        "nextRotation": GraphQLField(
            GraphQLNonNull(datetime_scalar),
            description="Returns when this rotation will next rotate.\n\n"
                        "If the rotation is due the exact time this method is called, "
                        "this method will return the next time that it will rotate.",
            args={
                "rotation": GraphQLArgument(
                    GraphQLNonNull(rotation_enum)
                )
            }
        ),
        "previousRotation": GraphQLField(
            GraphQLNonNull(datetime_scalar),
            description="Returns when this rotation last rotated.\n\n"
                        "If the rotation is due the exact time this method is called, "
                        "this method will return the current time.",
            args={
                "rotation": GraphQLArgument(
                    GraphQLNonNull(rotation_enum)
                )
            }
        )
    }
)

server_type = GraphQLObjectType(
    name="Server",
    description="A server on the network.",
    fields=lambda: {
        "associatedGame": GraphQLField(
            game_enum,
            description="The game associated with this server, if any."
        ),
        "category": GraphQLField(
            GraphQLNonNull(server_category_enum),
            description="The category of the server."
        ),
        "subType": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The sub-type of the server that can hold additional information about the server."
        )
    }
)

social_type = GraphQLObjectType(
    name="Social",
    description="Social data.",
    fields={
        "friends": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(player_type))),
            description="A list of the player's friends."
        ),
        "party": GraphQLField(
            GraphQLNonNull(party_type),
            description="The player's party."
        )
    }
)

statistic_type = GraphQLObjectType(
    name="Statistic",
    description="A statistic.",
    fields={
        "forLeaderboard": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="If this statistic generates leaderboards."
        ),
        "key": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The key of the statistic."
        ),
        "leaderboard": GraphQLField(
            GraphQLList(GraphQLNonNull(leaderboard_entry_type)),
            description="Returns the leaderboard for this statistic in a given rotation.\n\n"
                        "If this statistic does not generate leaderboards, "
                        "or the statistic is not tracked for the provided rotation, this will return `null`.",
            args={
                "amount": GraphQLArgument(
                    GraphQLNonNull(GraphQLInt),
                    default_value=10
                ),
                "rotation": GraphQLArgument(
                    GraphQLNonNull(rotation_enum),
                    default_value=rotation_enum.values["LIFETIME"].value
                )
            }
        ),
        "rotations": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(rotation_enum))),
            description="The rotations for which this statistic is tracked.\n\n"
                        "These are the rotations that can be used to generate leaderboards or fetch rotation values.\n"
                        "Note that the `YEARLY` rotation never generates leaderboards, "
                        "even if it is returned in this list."
        )
    }
)

statistic_value_result_type = GraphQLObjectType(
    name="StatisticValueResult",
    description="The result of fetching a value of a statistic.",
    fields={
        "statistic": GraphQLField(
            GraphQLNonNull(statistic_type),
            description="The statistic."
        ),
        "value": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The value."
        )
    }
)

statistics_type = GraphQLObjectType(
    name="Statistics",
    description="Statistic-related data.",
    fields={
        "rotationValue": GraphQLField(
            GraphQLInt,
            description="Returns the value stored for the given statistic in a rotation.\n\n"
                        "The returned number will be `null` if the statistic does not track in the provided rotation, "
                        "or if the statistic doesn't exist.",
            args={
                "rotation": GraphQLArgument(
                    GraphQLNonNull(rotation_enum),
                    default_value=rotation_enum.values["LIFETIME"].value
                ),
                "statisticKey": GraphQLArgument(
                    GraphQLNonNull(GraphQLString)
                )
            }
        )
    }
)

status_type = GraphQLObjectType(
    name="Status",
    description="A player's current status.",
    fields={
        "firstJoin": GraphQLField(
            datetime_scalar,
            description="When the player first joined MCC Island, if known."
        ),
        "lastJoin": GraphQLField(
            datetime_scalar,
            description="When the player most recently joined MCC Island, if known."
        ),
        "online": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="Whether the player is online or not."
        ),
        "server": GraphQLField(
            server_type,
            description="The player's current server, populated if they are online."
        )
    }
)

trophy_data_type = GraphQLObjectType(
    name="TrophyData",
    description="Data on the amount of trophies a user has/can have.",
    fields={
        "bonus": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount of bonus trophies."
        ),
        "obtainable": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The maximum amount of trophies that can be obtained."
        ),
        "obtained": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount of trophies obtained."
        )
    }
)

# Despite being an internal type, defining SpectaQLOption means that no breaking changes
# will be found when comparing this schema to that available from the API itself.
spectaqloption_type = GraphQLInputObjectType(
    name="SpectaQLOption",
    description="Internal key/value pair for documentation options.",
    fields={
        "key": GraphQLInputField(
            GraphQLNonNull(GraphQLString)
        ),
        "value": GraphQLInputField(
            GraphQLNonNull(GraphQLString)
        )
    }
)
