from .. import __user_agent
from .enums import (
    Game,
    Team
)
from .responses import (
    EventInformationResponse,
    EventsResponse,
    HallOfFameGameResponse,
    HallOfFameResponse,
    ParticipantResponse,
    ParticipantsResponse,
    ParticipantsTeamResponse,
    RundownResponse
)
import ratelimit
import requests
import typing as t
import warnings

__all__ = [
    "get_event",
    "get_events",
    "get_hall_of_fame",
    "get_rundown",
    "get_participant",
    "get_participants",

    "enums",
    "exceptions",
    "responses"
]

__base_url: t.Final[str] = "https://api.mcchampionship.com/v1"


@ratelimit.sleep_and_retry
@ratelimit.limits(calls=200, period=60)
def __request(endpoint: str, timeout: int) -> requests.Response:
    """Make and return a request to the given endpoint of the MCC API.
    
    Limited to 200 calls per minute, and will sleep until the rate limit resets if exceeded.
    Timeout parameter is passed to requests module directly."""
    return requests.get(
        f"{__base_url.rstrip('/')}/{endpoint}",
        headers={"User-Agent": __user_agent},
        timeout=timeout
    )


def get_event(*, timeout: int = 5) -> EventInformationResponse:
    """Get event data for the current event cycle.
    
    - Calls the `/event <https://api.mcchampionship.com/docs/#/v1/AppController_getEventInformation>`_ endpoint.
    - Returns an :class:`mcc_api.EventInformationResponse` representing the current event cycle's event.
    - May raise a :class:`requests.Timeout` exception, with the number of seconds before timing out specified by the
      `timeout` parameter and defaulting to 5.
    """
    return EventInformationResponse(__request("event", timeout))


def get_events(*, timeout: int = 5) -> EventsResponse:
    """Get all event keys currently made available by the API.

    - Calls the `/events <https://api.mcchampionship.com/docs/#/v1/AppController_getEventKeys>_ endpoint.
    - Returns an :class:`mcc_api.EventsResponse` containing all available event keys.
    - May raise a :class:`requests.Timeout` exception, with the number of seconds before timing out specified by the
    `timeout` parameter and defaulting to 5.
    """
    return EventsResponse(__request("events", timeout))


@t.overload
def get_hall_of_fame(*, timeout: int = 5) -> HallOfFameResponse: ...
@t.overload
def get_hall_of_fame(game: Game, *, timeout: int = 5) -> HallOfFameGameResponse: ...


def get_hall_of_fame(game: t.Optional[Game] = None, *, timeout: int = 5):
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

    In either case:
        - May raise a :class:`requests.Timeout` exception, with the number of seconds before timing out specified by the
          `timeout` parameter and defaulting to 5.

    .. warning::
       The /halloffame endpoint is deprecated and will be removed in a future release of the API.
       See https://github.com/Noxcrew/mcchampionship-api/releases/tag/v1.3.0
    """
    warnings.warn("The /halloffame endpoint is deprecated and will be removed in a future release of the API. "
                  "See https://github.com/Noxcrew/mcchampionship-api/releases/tag/v1.3.0",
                  DeprecationWarning, stacklevel=2)
    if game:
        return HallOfFameGameResponse(__request(f"halloffame/{game}", timeout))
    else:
        return HallOfFameResponse(__request("halloffame", timeout))


def get_rundown(event: t.Optional[str] = None, *, timeout: int = 5) -> RundownResponse:
    """Get an event's rundown data.

    When called with no `event` parameter:
        - Calls the `/rundown <https://api.mcchampionship.com/docs/#/v1/AppController_getRundown>`_ endpoint.
        - Returns a :class:`mcc_api.RundownResponse` representing the latest event.

    When called with an `event` parameter:
        - Calls the `/rundown/{event} <https://api.mcchampionship.com/docs/#/v1/AppController_getEventRundown>`_
          endpoint.
        - Returns a :class:`mcc_api.RundownResponse` representing the given event.
        - May raise an :class:`mcc_api.exceptions.InvalidEventError` exception.

    In either case:
        - May raise a :class:`requests.Timeout` exception, with the number of seconds before timing out specified by the
          `timeout` parameter and defaulting to 5.
    """
    if event:
        return RundownResponse(__request(f"rundown/{event}", timeout))
    else:
        return RundownResponse(__request("rundown", timeout))


def get_participant(uuid: str, *, timeout: int = 5) -> ParticipantResponse:
    """Get an individual participant in the current event cycle by their Minecraft UUID.

    - Accepts both dashed (e.g. 3e7a89ee-c4e2-4392-a317-444b861b0794) and un-dashed
      (e.g. 3e7a89eec4e24392a317444b861b0794) UUIDs
    - Calls the `/participant <https://api.mcchampionship.com/docs/#/v1/AppController_getParticipant>`_ endpoint.
    - Returns an :class:`mcc_api.ParticipantResponse` representing the individual participant in the current event
      cycle's event.
    - May raise a :class:`requests.Timeout` exception, with the number of seconds before timing out specified by the
      `timeout` parameter and defaulting to 5.
    """
    return ParticipantResponse(__request(f"participant/{uuid}", timeout))


@t.overload
def get_participants(*, timeout: int = 5) -> ParticipantsResponse: ...
@t.overload
def get_participants(team: Team, *, timeout: int = 5) -> ParticipantsTeamResponse: ...


def get_participants(team: t.Optional[Team] = None, *, timeout: int = 5):
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

    In either case:
        - May raise a :class:`requests.Timeout` exception, with the number of seconds before timing out specified by the
          `timeout` parameter and defaulting to 5.
    """
    if team:
        return ParticipantsTeamResponse(__request(f"participants/{team}", timeout))
    else:
        return ParticipantsResponse(__request("participants", timeout))
