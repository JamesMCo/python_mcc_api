from .enums import *
from .scalars import *
from graphql import (
    GraphQLArgument, GraphQLBoolean, GraphQLField, GraphQLInputField, GraphQLInputObjectType,
    GraphQLInt, GraphQLList, GraphQLNonNull, GraphQLObjectType, GraphQLString
)


__all__ = [
    "collections_type",
    "crown_level_type",
    "currency_type",
    "leaderboard_entry_type",
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


collections_type = GraphQLObjectType(
    name="Collections",
    description="Collections data.",
    fields=lambda: {
        "currency": GraphQLField(
            GraphQLNonNull(currency_type),
            description="The player's earned currency."
        )
    }
)

crown_level_type = GraphQLObjectType(
    name="CrownLevel",
    description="A Crown Level and associated trophy data.",
    fields=lambda: {
        "level": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The overall Crown Level."
        ),
        "nextEvolutionLevel": GraphQLField(
            GraphQLInt,
            description="The next level that the crown will evolve, if any."
        ),
        "nextLevelProgress": GraphQLField(
            progression_data_type,
            description="The progress the player is making towards their next level, if any."
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
        "coins": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of coins the player currently has."
        ),
        "gems": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of gems the player currently has."
        ),
        "materialDust": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount of material dust the player currently has."
        ),
        "royalReputation": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount of Royal Reputation the player currently has."
        ),
        "silver": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount of silver the player currently has."
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
        "value": GraphQLField(
            statistic_value_result_type,
            description="Returns the raw value stored for this statistic.",
            args={
                "statisticKey": GraphQLArgument(
                    GraphQLNonNull(GraphQLString)
                )
            },
            deprecation_reason="This value is not backed by a rotation and will be removed. "
                               "Use `rotationValue` instead."
        ),
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
