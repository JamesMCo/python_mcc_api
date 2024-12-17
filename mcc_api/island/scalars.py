from datetime import date, datetime
from graphql import GraphQLScalarType, ValueNode
from graphql.utilities import value_from_ast_untyped
from uuid import UUID
import typing as t


__all__ = [
    "date_scalar", "datetime_scalar", "uuid_scalar"
]


# Date scalar based on datetime example in gql library documentation
# https://gql.readthedocs.io/en/latest/usage/custom_scalars_and_enums.html

def date_serialize(value: date) -> str:
    return value.isoformat()


def date_parse_value(value: str) -> date:
    return date.fromisoformat(value)


def date_parse_literal(value_node: ValueNode, variables: t.Optional[dict[str, t.Any]] = None) -> date:
    ast_value = value_from_ast_untyped(value_node, variables)
    return date_parse_value(ast_value)


date_scalar = GraphQLScalarType(
    name="Date",
    description="An RFC-3339 compliant Full Date Scalar",
    specified_by_url="https://tools.ietf.org/html/rfc3339",
    serialize=date_serialize,
    parse_value=date_parse_value,
    parse_literal=date_parse_literal
)


# Datetime scalar from example in gql library documentation
# https://gql.readthedocs.io/en/latest/usage/custom_scalars_and_enums.html

def datetime_serialize(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds")


def datetime_parse_value(value: str) -> datetime:
    return datetime.fromisoformat(value)


def datetime_parse_literal(value_node: ValueNode, variables: t.Optional[dict[str, t.Any]] = None) -> datetime:
    ast_value = value_from_ast_untyped(value_node, variables)
    return datetime_parse_value(ast_value)


datetime_scalar = GraphQLScalarType(
    name="DateTime",
    description="A slightly refined version of RFC-3339 compliant DateTime Scalar",
    specified_by_url="https://scalars.graphql.org/andimarek/date-time.html",
    serialize=datetime_serialize,
    parse_value=datetime_parse_value,
    parse_literal=datetime_parse_literal
)


# UUID scalar based on datetime example in gql library documentation
# https://gql.readthedocs.io/en/latest/usage/custom_scalars_and_enums.html

def uuid_serialize(value: UUID) -> str:
    return str(value)


def uuid_parse_value(value: str) -> UUID:
    return UUID(value)


def uuid_parse_literal(value_node: ValueNode, variables: t.Optional[dict[str, t.Any]] = None) -> UUID:
    ast_value = value_from_ast_untyped(value_node, variables)
    return uuid_parse_value(ast_value)


uuid_scalar = GraphQLScalarType(
    name="UUID",
    description="A universally unique identifier compliant UUID Scalar",
    specified_by_url="https://tools.ietf.org/html/rfc4122",
    serialize=uuid_serialize,
    parse_value=uuid_parse_value,
    parse_literal=uuid_parse_literal
)
