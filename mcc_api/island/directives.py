from .types import spectaqloption_type
from graphql import DirectiveLocation, GraphQLArgument, GraphQLDirective, GraphQLList


__all__ = [
    "one_of_directive", "spectaql_directive"
]

# oneOf is not one of the directives defined by the GraphQL specification, and thus
# needs to be defined in order to avoid breaking changed being found when comparing
# this schema to that available from the API itself.
one_of_directive = GraphQLDirective(
    name="oneOf",
    description="Indicates an Input Object is a OneOf Input Object.",
    locations=[DirectiveLocation.INPUT_OBJECT]
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
