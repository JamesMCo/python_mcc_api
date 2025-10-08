from .enums import *
from .interfaces import *
from .scalars import *
from graphql import (
    GraphQLArgument, GraphQLBoolean, GraphQLField, GraphQLInputField, GraphQLInputObjectType,
    GraphQLInt, GraphQLList, GraphQLNonNull, GraphQLObjectType, GraphQLString, GraphQLUnionType
)


__all__ = [
    "auction_listing_type",
    "badge_type",
    "badge_progress_type",
    "badge_stage_type",
    "badge_stage_progress_type",
    "collections_type",
    "cosmetic_type",
    "cosmetic_ownership_state_type",
    "cosmetic_token_type",
    "crown_level_type",
    "currency_type",
    "faction_type",
    "fish_type",
    "fish_caught_weight_type",
    "fish_record_type",
    "general_goal_type",
    "global_leaderboard_entry_type",
    "goal_type",
    "island_exchange_listing_type",
    "leaderboard_entry_type",
    "level_data_type",
    "mcc_plus_status_type",
    "party_type",
    "player_type",
    "progression_data_type",
    "query_type",
    "quest_type",
    "royal_reputation_type",
    "server_type",
    "simple_asset_type",
    "social_type",
    "statistic_type",
    "statistic_progress_type",
    "statistic_value_result_type",
    "statistics_type",
    "status_type",
    "spectaqloption_type",
    "trophy_data_type"
]

auction_listing_type = GraphQLObjectType(
    name="AuctionListing",
    description="An auction listing.",
    fields={
        "asset": GraphQLField(
            GraphQLNonNull(asset_interface),
            description="The asset that is being auctioned."
        ),
        "cost": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The current cost of the auction."
        ),
        "endTime": GraphQLField(
            GraphQLNonNull(datetime_scalar),
            description="The time this auction will end."
        ),
        "identifier": GraphQLField(
            GraphQLNonNull(uuid_scalar),
            description="A unique identifier for this listing.\n\n"
                        "This can be used to deduplicate listings if storing externally."
        ),
        "lastUpdateTime": GraphQLField(
            GraphQLNonNull(datetime_scalar),
            description="The time this auction received a bid or the start time if no bids have been made yet."
        )
    }
)

badge_type = GraphQLObjectType(
    name="Badge",
    description="A badge.",
    fields=lambda: {
        "goal": GraphQLField(
            GraphQLNonNull(goal_type),
            description="The goal this badge requires."
        ),
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of the badge."
        ),
        "stages": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(badge_stage_type))),
            description="The stages of this badge."
        )
    }
)

badge_progress_type = GraphQLObjectType(
    name="BadgeProgress",
    description="A badge with its progress",
    fields=lambda: {
        "badge": GraphQLField(
            GraphQLNonNull(badge_type),
            description="The badge itself."
        ),
        "stageProgress": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(badge_stage_progress_type))),
            description="The progress of each stage of the badge."
        )
    }
)

badge_stage_type = GraphQLObjectType(
    name="BadgeStage",
    description="A stage in a badge.",
    fields={
        "bonusTrophies": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of bonus trophies this stage gives."
        ),
        "stage": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The stage of the badge."
        ),
        "trophies": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of trophies this stage gives."
        )
    }
)

badge_stage_progress_type = GraphQLObjectType(
    name="BadgeStageProgress",
    description="The progress of a badge stage.",
    fields=lambda: {
        "progress": GraphQLField(
            GraphQLNonNull(progression_data_type),
            description="The progress."
        ),
        "stage": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The stage of the badge."
        )
    }
)

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
    interfaces=[asset_interface],
    description="A cosmetic.",
    fields=lambda: {
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
        "obtainmentHint": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="A hint as to how this cosmetic can be obtained."
        ),
        "rarity": GraphQLField(
            GraphQLNonNull(rarity_enum),
            description="The rarity of the cosmetic."
        ),
        "royalReputation": GraphQLField(
            royal_reputation_type,
            description="Information about the Royal Reputation this cosmetic provides.\n\n"
                        "This will be `null` if the cosmetic cannot be donated."
        ),
        "trophies": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of trophies this cosmetic awards.\n\n"
                        "Note that this does not include the completion bonus for applying all "
                        "Chroma Packs to the cosmetic."
        ),
        "type": GraphQLField(
            GraphQLNonNull(cosmetic_type_enum),
            description="The type of this cosmetic."
        ),
        "uniqueIdentifier": GraphQLField(
            GraphQLNonNull(uuid_scalar),
            description="A unique identifier for this specific type of asset.\n\n"
                        "This is based on the internal identifier for this asset and can be used "
                        "to track it over time.\n"
                        "For example, if the name of this asset changed, the identifier would remain the same."
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

cosmetic_token_type = GraphQLObjectType(
    name="CosmeticToken",
    interfaces=[asset_interface],
    description="A cosmetic token.",
    fields={
        "cosmetic": GraphQLField(
            GraphQLNonNull(cosmetic_type),
            description="The cosmetic this token holds."
        ),
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of this cosmetic token."
        ),
        "rarity": GraphQLField(
            GraphQLNonNull(rarity_enum),
            description="The rarity of this asset."
        ),
        "uniqueIdentifier": GraphQLField(
            GraphQLNonNull(uuid_scalar),
            description="A unique identifier for this specific type of asset.\n\n"
                        "This is based on the internal identifier for this asset and can be used "
                        "to track it over time.\n"
                        "For example, if the name of this asset changed, the identifier would remain the same."
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
        "styleLevelData": GraphQLField(
            GraphQLNonNull(level_data_type),
            description="The style level data."
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
        "royalReputation": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The number of Royal Reputation the player currently has."
        )
    }
)

faction_type = GraphQLObjectType(
    name="Faction",
    description="Information about a faction.",
    fields=lambda: {
        "levelData": GraphQLField(
            GraphQLNonNull(level_data_type),
            description="The faction level data."
        ),
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of this faction."
        ),
        "selected": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="Whether this faction is currently the selected faction for the player."
        ),
        "totalExperience": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The total amount of experience the player has."
        )
    }
)

fish_type = GraphQLObjectType(
    name="Fish",
    interfaces=[asset_interface],
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
        "sellingPrice": GraphQLField(
            GraphQLInt,
            description="The number of A.N.G.L.R. Tokens given for selling this fish in a given weight.",
            args={
                "weight": GraphQLArgument(
                    GraphQLNonNull(fish_weight_enum)
                )
            }
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
        "uniqueIdentifier": GraphQLField(
            GraphQLNonNull(uuid_scalar),
            description="A unique identifier for this specific type of asset.\n\n"
                        "This is based on the internal identifier for this asset and can be used "
                        "to track it over time.\n"
                        "For example, if the name of this asset changed, the identifier would remain the same."
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

general_goal_type = GraphQLObjectType(
    name="GeneralGoal",
    description="A goal that isn't tied to a statistic.",
    fields={
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of this goal."
        )
    }
)

global_leaderboard_entry_type = GraphQLObjectType(
    name="GlobalLeaderboardEntry",
    description="A global leaderboard entry.\n\n"
                "This is used for leaderboards that do not have players as entries, "
                "e.g. the global faction leaderboard.",
    fields={
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of this entry."
        ),
        "rank": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The rank of this entry."
        ),
        "value": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The value of this entry."
        )
    }
)

goal_type = GraphQLUnionType(
    name="Goal",
    description="A goal.",
    types=lambda: [
        statistic_type,
        general_goal_type
    ]
)

island_exchange_listing_type = GraphQLObjectType(
    name="IslandExchangeListing",
    description="A listing in the Island Exchange.",
    fields={
        "amount": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount of the asset that is being sold."
        ),
        "asset": GraphQLField(
            GraphQLNonNull(asset_interface),
            description="The asset that is being sold."
        ),
        "cost": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The cost of purchasing this listing."
        ),
        "creationTime": GraphQLField(
            GraphQLNonNull(datetime_scalar),
            description="The time this listing was created."
        ),
        "endTime": GraphQLField(
            GraphQLNonNull(datetime_scalar),
            description="The time this listing will expire (if the listing is active) or the time it sold."
        ),
        "identifier": GraphQLField(
            GraphQLNonNull(uuid_scalar),
            description="A unique identifier for this entry.\n\n"
                        "This can be used to deduplicate listings if storing externally."
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
                        "However, for Crown Level or Trophy count leaderboards, the player will not be `null`.\n"
                        "It will also never be `null` for players with a rank less than or equal to 10."
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
        "badges": GraphQLField(
            GraphQLList(GraphQLNonNull(badge_progress_type)),
            description="The badges for the player.\n\n"
                        "A list of badges and the progress each badge stage has.\n\n"
                        "This method is conditional on the player having the in-game "
                        "\"statistics\" API setting enabled."
        ),
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
        "factions": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(faction_type))),
            description="Faction data for the player.\n\n"
                        "A list with all factions data for the player, including level, experience, "
                        "and whether is is the currently selected faction."
        ),
        "mccPlusStatus": GraphQLField(
            mcc_plus_status_type,
            description="The player's MCC+ status, if currently subscribed."
        ),
        "quests": GraphQLField(
            GraphQLList(GraphQLNonNull(quest_type)),
            description="The quests for the player.\n\n"
                        "A list of quests the player currently has, this includes completed quests "
                        "and currently active quests, including scrolls.\n\n"
                        "This method is conditional on the player having the in-game "
                        "\"quests\" API setting enabled."
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
        "badges": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(badge_type))),
            description="Returns a list of all known badges."
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
        ),
        "activeIslandExchangeListings": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(island_exchange_listing_type))),
            description="Returns a list of all active Island Exchange listings.\n\n"
                        "This endpoint will not return listings until they have been "
                        "active for a certain length of time.\n"
                        "This is to help prevent sniping/botting and to ensure server "
                        "players have priority of website/bot users."
        ),
        "soldIslandExchangeListings": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(island_exchange_listing_type))),
            description="Returns a list of all Island Exchange sales made in the last 24 hours.\n\n"
                        "This only includes listings that sold successfully.\n"
                        "Listings that did not sell or are still active are not included in this."
        ),
        "activeAuctionListings": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(auction_listing_type))),
            description="Returns a list of all active auctions.\n\n"
                        "This includes items being sold in the Grand Auction as well as other auctions "
                        "(such as event auctions)."
        ),
        "factionLeaderboard": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(global_leaderboard_entry_type))),
            description="Returns the global faction leaderboard.\n\n"
                        "This leaderboard ranks all factions by the amount of XP players have gained in that faction.\n"
                        "The values returned are a percentage of all XP earned in all factions.\n"
                        "For example, if Red Rabbits returned a value of 15, "
                        "that would mean they have 15% of all faction XP.\n"
                        "As all percentages are rounded down, the values may not sum to 100%."
        )
    }
)

quest_type = GraphQLObjectType(
    name="Quest",
    description="Information about a quest.",
    fields=lambda: {
        "boost": GraphQLField(
            GraphQLNonNull(boost_type_enum),
            description="The boost type."
        ),
        "completed": GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            description="If this quest is completed or not."
        ),
        "rarity": GraphQLField(
            GraphQLNonNull(rarity_enum),
            description="The rarity."
        ),
        "tasks": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(statistic_progress_type))),
            description="The tasks this quest has."
        ),
        "type": GraphQLField(
            GraphQLNonNull(quest_type_enum),
            description="The type of the quest."
        )
    }
)

royal_reputation_type = GraphQLObjectType(
    name="RoyalReputation",
    description="Information about the Royal Reputation for a cosmetic.",
    fields={
        "donationLimit": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The maximum number of donations that can be made for this cosmetic."
        ),
        "reputationAmount": GraphQLField(
            GraphQLNonNull(GraphQLInt),
            description="The amount of reputation that each donation provides."
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

simple_asset_type = GraphQLObjectType(
    name="SimpleAsset",
    interfaces=[asset_interface],
    description="A simple implementation of an asset.\n\n"
                "This type is used for when there is no other concrete implementation "
                "of asset that is better suited to be returned.",
    fields={
        "name": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The name of this asset."
        ),
        "rarity": GraphQLField(
            GraphQLNonNull(rarity_enum),
            description="The rarity of this asset."
        ),
        "uniqueIdentifier": GraphQLField(
            GraphQLNonNull(uuid_scalar),
            description="A unique identifier for this specific type of asset.\n\n"
                        "This is based on the internal identifier for this asset and can be used "
                        "to track it over time.\n"
                        "For example, if the name of this asset changed, the identifier would remain the same."
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
                        "or the statistic is not tracked for the provided rotation, this will return `null`.\n\n"
                        "Both the `amount` and `offset` fields are coerced lower than arbitrary maximum values "
                        "which may change at any time.\n\n"
                        "The amount of returned entries may be larger than `amount`.\n"
                        "This is because the `amount` field determines the number of placements "
                        "to return and multiple users may be tied on the same placement.",
            args={
                "amount": GraphQLArgument(
                    GraphQLNonNull(GraphQLInt),
                    default_value=10
                ),
                "offset": GraphQLArgument(
                    GraphQLNonNull(GraphQLInt),
                    default_value=0
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

statistic_progress_type = GraphQLObjectType(
    name="StatisticProgress",
    description="The progress of a statistic on a progression value.",
    fields={
        "progress": GraphQLField(
            GraphQLNonNull(progression_data_type),
            description="The progress."
        ),
        "statistic": GraphQLField(
            GraphQLNonNull(statistic_type),
            description="The statistic."
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
