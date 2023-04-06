from .enums import (
    Game,
    Team
)
from .responses import (
    EventInformationResponse,
    HallOfFameGameResponse,
    HallOfFameResponse,
    ParticipantsResponse,
    ParticipantsTeamResponse,
    RundownResponse
)
import ratelimit
import requests
import typing as t
import warnings

__version__ = "1.0.0"

__base_url: t.Final[str] = "https://api.mcchampionship.com/v1"
__user_agent: t.Final[str] = f"python_mcc_api/{__version__} (https://github.com/JamesMCo/python_mcc_api)"


@ratelimit.sleep_and_retry
@ratelimit.limits(calls=40, period=60)
def __request(endpoint: str) -> requests.Response:
    """Make and return a request to the given endpoint of the MCC API.
    
    Limited to 40 calls per minute, and will sleep until the rate limit resets if exceeded."""
    return requests.get(f"{__base_url.rstrip('/')}/{endpoint}", headers={"User-Agent": __user_agent})


def get_event() -> EventInformationResponse:
    """Get event data for the current event cycle.
    
    - Calls the `/event <https://api.mcchampionship.com/docs/#/v1/AppController_getEventInformation>`_ endpoint.
    - Returns an :class:`mcc_api.EventInformationResponse` representing the current event cycle's event.
    """
    return EventInformationResponse(__request("event"))


@t.overload
def get_hall_of_fame() -> HallOfFameResponse: ...
@t.overload
def get_hall_of_fame(game: Game) -> HallOfFameGameResponse: ...


def get_hall_of_fame(game: t.Optional[Game] = None):
    """Get hall of fame data, optionally restricted to a single game.
    
    When called with no `game` parameter:
        - Calls the `/halloffame <https://api.mcchampionship.com/docs/#/[Deprecated]%20v1/AppController_getHallOfFame>`_
          endpoint.
        - Returns a :class:`mcc_api.HallOfFameResponse` representing the entire Hall of Fame.

    When called with a `game` parameter:
        - Calls the `/halloffame/{game}
          <https://api.mcchampionship.com/docs/#/[Deprecated]%20v1/AppController_getHallOfFameByGame>`_ endpoint.
        - Returns a :class:`mcc_api.HallOfFameGameResponse` representing a single game from the Hall of Fame.
        - May raise an :class:`mcc_api.exceptions.InvalidGameError` exception, which can be avoided by passing an
          :class:`mcc_api.Game` enum.

    .. warning::
       The /halloffame endpoint is deprecated and will be removed in a future release of the API.
       See https://github.com/Noxcrew/mcchampionship-api/releases/tag/v1.3.0
    """
    warnings.warn("The /halloffame endpoint is deprecated and will be removed in a future release of the API. "
                  "See https://github.com/Noxcrew/mcchampionship-api/releases/tag/v1.3.0",
                  DeprecationWarning)
    if game:
        return HallOfFameGameResponse(__request(f"halloffame/{game}"))
    else:
        return HallOfFameResponse(__request("halloffame"))


def get_rundown(event: t.Optional[str] = None) -> RundownResponse:
    """Get an event's rundown data.

    When called with no `event` parameter:
        - Calls the `/rundown <https://api.mcchampionship.com/docs/#/v1/AppController_getRundown>`_ endpoint.
        - Returns a :class:`mcc_api.RundownResponse` representing the latest event.

    When called with an `event` parameter:
        - Calls the `/rundown/{event} <https://api.mcchampionship.com/docs/#/v1/AppController_getEventRundown>`_
          endpoint.
        - Returns a :class:`mcc_api.RundownResponse` representing the given event.
        - May raise an :class:`mcc_api.exceptions.InvalidEventError` exception.
    """
    if event:
        return RundownResponse(__request(f"rundown/{event}"))
    else:
        return RundownResponse(__request("rundown"))


@t.overload
def get_participants() -> ParticipantsResponse: ...
@t.overload
def get_participants(team: Team) -> ParticipantsTeamResponse: ...


def get_participants(team: t.Optional[Team] = None):
    """Get the participants in the current event cycle.
    
    When called with no `team` parameter:
        - Calls the `/participants <https://api.mcchampionship.com/docs/#/v1/AppController_getParticipants>`_ endpoint.
        - Returns a :class:`mcc_api.ParticipantsResponse` representing all teams and their participants in the current
          event cycle.

    When called with a `team` parameter:
        - Calls the `/participants/{team}
          <https://api.mcchampionship.com/docs/#/v1/AppController_getParticipantsByTeam>`_ endpoint.
        - Returns a :class:`mcc_api.ParticipantsTeamResponse` representing the given team and its participants in the
          current event cycle.
        - May raise an :class:`mcc_api.exceptions.InvalidTeamError` exception, which can be avoided by passing an
          :class:`mcc_api.Team` enum.
    """
    if team:
        return ParticipantsTeamResponse(__request(f"participants/{team}"))
    else:
        return ParticipantsResponse(__request("participants"))
