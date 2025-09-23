from .enums import *
from .scalars import uuid_scalar
from graphql import GraphQLField, GraphQLInterfaceType, GraphQLNonNull, GraphQLString


__all__ = [
    "asset_interface"
]

asset_interface = GraphQLInterfaceType(
    name="Asset",
    description="An asset.\n\n"
                "Effectively, an asset encompasses all forms of items on the Island.\n"
                "This includes Cosmetics, openables, materials, fish, etc.\n"
                "Basically anything that can fit in your Infinibag!",
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
