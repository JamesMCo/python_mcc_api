from .. import __user_agent
from .auth import APIKey
from .directives import *
from .enums import *
from .types import *
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from graphql import GraphQLSchema, specified_directives
import typing as t


__all__ = ["client", "set_api_key"]

__base_url: t.Final[str] = "https://api.mccisland.net/graphql"

schema = GraphQLSchema(
    query=query_type,
    directives=[*specified_directives, one_of_directive, spectaql_directive],
    types=[
        collections_type,
        crown_level_type,
        currency_type,
        leaderboard_entry_type,
        party_type,
        player_type,
        progression_data_type,
        query_type,
        server_type,
        social_type,
        statistic_type,
        statistic_value_result_type,
        statistics_type,
        status_type,
        spectaqloption_type,
        trophy_data_type,

        game_enum,
        rank_enum,
        rotation_enum,
        server_category_enum,
        trophy_category_enum,
    ]
)

_transport = RequestsHTTPTransport(
    url=__base_url,
    headers={"User-Agent": __user_agent}
)

client = Client(transport=_transport, schema=schema, serialize_variables=True, parse_results=True)
"""An instance of :external:class:`gql.Client` configured to make requests to the MCC Island API.

Must be provided an API key using :py:func:`.set_api_key`,
otherwise requests will be rejected with an HTTP 401 status code by the API.

Queries can be executed by passing the result of :external:py:func:`gql.gql` object to
:external:py:meth:`client.execute() <gql.client.Client.execute>`. Queries are verified to be valid using according to
the schema before being sent to the API, raising a
:external:py:class:`graphql.GraphQLError <graphql.error.graphql_error.GraphQLError>` if not. The returned data will be a
Python dictionary whose structure matches that of the query. Data returned as a UUID, a Date, or a DateTime will be
resolved as a :external:py:class:`UUID <.uuid.UUID>`, a :external:py:class:`date <.datetime.date>`, or a
:external:py:class:`datetime <.datetime.datetime>` object respectively. Some data may not be present if the user being
queried has kept some of their data private to the API.

.. note::
    All API settings (collections, social, statistics, and status) are opt-in, and so all related data will be
    private unless a player has explicitly chosen to enable them.

For example, to calculate the win percentage for a player in Parkour Warrior: Survivor, the following code
could be used:

.. code-block:: python

    from gql import gql
    from mcc_api.island import client, set_api_key
    
    set_api_key("<YOUR_API_KEY>")
    
    query = gql(\"""
        query pkwStats($username: String!) {
            playerByUsername(username: $username) {
                username
                statistics {
                    total_games: value(statisticKey: "pw_survival_games_played") { value }
                    total_wins: value(statisticKey: "pw_survival_final_duel_wins") { value }
                }
            }
        }
    \""")
    
    data = client.execute(query, variable_values={"username": "Jammy4312"})
    player = data["playerByUsername"]
    
    username = player["username"]
    if "statistics" in player:
        total_games = player["statistics"]["total_games"]["value"]
        total_wins = player["statistics"]["total_wins"]["value"]
        win_rate = (total_wins / total_games) * 100 if total_games > 0 else 0
    
        print(f"{username} has won {win_rate}% of their {total_games} Parkour Warrior: Survivor games.")
    else:
        print(f"{username}'{'' if username[-1].lower() == 's' else 's'} collections are private.")
"""


def set_api_key(api_key: str) -> None:
    """Set the API key to use as authentication for all future requests to the MCC Island API.

    API keys can be minted using `Noxcrew Gateway <https://gateway.noxcrew.com>`_."""

    _transport.auth = APIKey(api_key)
