from .types import spectaqloption_type
from graphql import (
    DEFAULT_DEPRECATION_REASON, DirectiveLocation, GraphQLArgument, GraphQLDirective, GraphQLList, GraphQLString
)


__all__ = [
    "deprecated_directive", "spectaql_directive"
]

# The locations defined by the graphql module's GraphQLDeprecatedDirective do not match those
# defined by the API's schema, so we need this version to prevent breaking changes being found.
deprecated_directive = GraphQLDirective(
    name="deprecated",
    description="The reason for the deprecation",
    args={
        "reason": GraphQLArgument(
            GraphQLString,
            default_value=DEFAULT_DEPRECATION_REASON
        )
    },
    locations=[
        DirectiveLocation.FIELD_DEFINITION,
        DirectiveLocation.ARGUMENT_DEFINITION,
        DirectiveLocation.ENUM_VALUE,
        DirectiveLocation.INPUT_FIELD_DEFINITION
    ]
)

# Despite being an internal directive, defining @spectaql means that no breaking changes
# will be found when comparing this schema to that available from the API itself.
spectaql_directive = GraphQLDirective(
    name="spectaql",
    description="Internal directive used to generate some documentation elements.",
    args={
        "options": GraphQLArgument(
            GraphQLList(spectaqloption_type)
        )
    },
    locations=[
        DirectiveLocation.QUERY, DirectiveLocation.MUTATION, DirectiveLocation.SUBSCRIPTION, DirectiveLocation.FIELD,
        DirectiveLocation.FRAGMENT_DEFINITION, DirectiveLocation.FRAGMENT_SPREAD, DirectiveLocation.INLINE_FRAGMENT,
        DirectiveLocation.VARIABLE_DEFINITION, DirectiveLocation.SCHEMA, DirectiveLocation.SCALAR,
        DirectiveLocation.OBJECT, DirectiveLocation.FIELD_DEFINITION, DirectiveLocation.ARGUMENT_DEFINITION,
        DirectiveLocation.INTERFACE, DirectiveLocation.UNION, DirectiveLocation.ENUM, DirectiveLocation.ENUM_VALUE,
        DirectiveLocation.INPUT_OBJECT, DirectiveLocation.INPUT_FIELD_DEFINITION
    ]
)
