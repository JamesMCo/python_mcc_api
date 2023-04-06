from .exceptions import InvalidEventError, InvalidGameError, InvalidTeamError, RateLimitError
from .enums import Game, Team
from dataclasses import dataclass
from datetime import datetime
import json
import requests
import typing as t


class BaseResponse:
    """The base response from which all other mcc_api responses inherit."""

    code: int
    """Response code of the request from the API."""
    reason: t.Optional[str]
    """Reason for the response code, if applicable."""
    __json: str

    def __init__(self: t.Self, request: requests.Response | dict[str, t.Any]) -> None:
        data: dict[str, t.Any] = self._extract_json_data(request)
        self.__json = json.dumps(data)

        self.code = data.get("code")
        self.reason = data.get("reason")

        if self.code == 429:
            raise RateLimitError(self.code, self.reason)

    @staticmethod
    def _extract_json_data(data: requests.Response | dict[str, t.Any]) -> dict[str, t.Any]:
        """Return json data from a requests.Response object, or return the input unchanged"""
        return data.json() if isinstance(data, requests.Response) else data

    @property
    def json(self: t.Self) -> str:
        """JSON string of the data returned by the API."""
        return self.__json


@dataclass(frozen=True, slots=True)
class EventInformationData:
    """The current event cycle's event data."""

    date: datetime
    """The date and time at which the event starts.
    
    Stored as an offset-aware datetime object.
    """
    event: str
    """The name of the event."""
    updateVideo: t.Optional[str]
    """The YouTube embed URL of the event's update video."""


class EventInformationResponse(BaseResponse):
    """Response object representing the current event cycle's event."""

    data: EventInformationData
    """Current event cycle's event data."""

    def __init__(self: t.Self, request: requests.Response | dict[str, t.Any]) -> None:
        data: dict[str, t.Any] = self._extract_json_data(request)
        super().__init__(data)

        self.data = EventInformationData(
            date=datetime.fromisoformat(data["data"]["date"]),
            event=data["data"]["event"],
            updateVideo=data["data"].get("updateVideo")
        )


@dataclass(frozen=True, slots=True)
class HallOfFameRecord:
    """A single record from the Hall of Fame.

    .. note::
       The name of the record is not kept within the record, and can instead be found in the :class:`HallOfFameResponse`
       or :class:`HallOfFameGameResponse` objects.
    """

    player: str
    """The username of the player that holds the record."""
    value: str | int
    """The value of the record."""
    placement: int
    """The placement value used internally by MCC.live."""
    changedHands: bool
    """Whether the record changed hands in the latest event."""


class HallOfFameResponse(BaseResponse):
    """Response object representing the entire Hall of Fame."""

    data: dict[Game, dict[str, HallOfFameRecord]]
    """Dictionary of games mapped to dictionaries of strings to Hall of Fame records.
    
    Keys in the inner dictionaries are strings that contain the names of the records themselves. For example:
    
    .. code-block:: python
    
       data = {
           mcc_api.Game.GLOBAL_STATISTICS: {
               "RECORD NAME 1": mcc_api.responses.HallOfFameRecord(
                   placement=0,
                   player="MCChampionship",
                   value="String value",
                   changedHands=False
               ),
               "RECORD NAME 2": mcc_api.responses.HallOfFameRecord(
                   placement=1,
                   player="MCChampionship",
                   value=0,
                   changedHands=True
               )
           },
           mcc_api.Game.LEGACY_STATISTICS: {
               "RECORD NAME 1": mcc_api.responses.HallOfFameRecord(
                   placement=0,
                   player="MCChampionship",
                   value="String value",
                   changedHands=False
               ),
               "RECORD NAME 2": mcc_api.responses.HallOfFameRecord(
                   placement=1,
                   player="MCChampionship",
                   value=0,
                   changedHands=True
               )
           }
       }
    """

    def __init__(self: t.Self, request: requests.Response | dict[str, t.Any]) -> None:
        data: dict[str, t.Any] = super()._extract_json_data(request)
        super().__init__(data)

        self.data = {
            Game[game]: {
                record_name: HallOfFameRecord(
                    player=record_data["player"],
                    value=record_data["value"],
                    placement=record_data["placement"],
                    changedHands=record_data["changedHands"]
                ) for record_name, record_data in game_records.items()
            } for game, game_records in data["data"].items()}


class HallOfFameGameResponse(BaseResponse):
    """Response object representing a single game from the Hall of Fame."""

    data: dict[str, HallOfFameRecord]
    """Dictionary of strings to Hall of Fame records.
    
    Keys in the dictionary are strings that contain the names of the records themselves. For example:
    
    .. code-block:: python
    
       data = {
           "RECORD NAME 1": mcc_api.responses.HallOfFameRecord(
               placement=0,
               player="MCChampionship",
               value="String value",
               changedHands=False
           ),
           "RECORD NAME 2": mcc_api.responses.HallOfFameRecord(
               placement=1,
               player="MCChampionship",
               value=0,
               changedHands=True
           )
       }
    """

    def __init__(self: t.Self, request: requests.Response | dict[str, t.Any]) -> None:
        data: dict[str, t.Any] = super()._extract_json_data(request)
        super().__init__(data)

        if self.code == 400:
            raise InvalidGameError(self.code, self.reason)

        self.data = {
            record_name: HallOfFameRecord(
                player=record_data["player"],
                value=record_data["value"],
                placement=record_data["placement"],
                changedHands=record_data["changedHands"]
            )
            for record_name, record_data in data["data"].items()}


@dataclass(frozen=True, slots=True)
class RundownHistoryGame:
    """Object representing score and placement data for a single game from a single event."""

    index: int
    """The number of the game in the event when this was played (zero-indexed)."""
    game: Game
    """The game that was played."""
    multiplier: float
    """The multiplier applied to coins earned during this game."""
    individualScores: t.Optional[dict[str, int]]
    """Dictionary mapping player usernames to their total coins after this game."""
    gameScores: t.Optional[dict[Team, int]]
    """Dictionary mapping teams to their coins earned during this game (multiplied)."""
    eventScores: t.Optional[dict[Team, int]]
    """Dictionary mapping teams to their total coins after this game."""
    gamePlacements: t.Optional[dict[Team, int]]
    """Dictionary mapping teams to their placement in this game (zero-indexed)."""
    eventPlacements: t.Optional[dict[Team, int]]
    """Dictionary mapping teams to their placement in the event after this game (zero-indexed)."""


@dataclass(frozen=True, slots=True)
class EventRundown:
    """Object representing score, game, and participant data for a single event."""

    dodgeboltData: dict[Team, int]
    """Dictionary mapping teams in Dodgebolt to the number of rounds of Dodgebolt that they won."""
    eventPlacements: dict[Team, int]
    """Dictionary mapping teams to their final placements in the event (zero-indexed)."""
    eventScores: dict[Team, int]
    """Dictionary mapping teams to their final coins totals."""
    individualScores: dict[str, int]
    """Dictionary mapping player usernames to their final coins totals."""
    history: dict[str, RundownHistoryGame]
    """Dictionary mapping game index to a RundownHistoryGame object (zero-indexed).
    
    Dictionary keys are the number of the game being played as a string. For example:
    
    .. code-block:: python
    
       data = {
           ...
           history: {
               # The first game in the event to be played:
               "0": mcc_api.responses.RundownHistoryGame(...),
               
               # The second game in the event to be played:
               "1": mcc_api.responses.RundownHistoryGame(...),
               ...
           }
           ...
       }
    """
    creators: dict[Team, list[str]]
    """Dictionary mapping teams to lists of their players' usernames."""


class RundownResponse(BaseResponse):
    """Response object representing score, game, and participant data for a single event."""

    data: EventRundown
    """Object representing the event's data."""

    def __init__(self: t.Self, request: requests.Response | dict[str, t.Any]) -> None:
        data: dict[str, t.Any] = super()._extract_json_data(request)
        super().__init__(data)

        if self.code == 400:
            raise InvalidEventError(self.code, self.reason)

        self.data = EventRundown(
            dodgeboltData={Team[team]: score for team, score in data["data"]["dodgeboltData"].items()},
            eventPlacements={Team[team]: placement for team, placement in data["data"]["eventPlacements"].items()},
            eventScores={Team[team]: score for team, score in data["data"]["eventScores"].items()},
            individualScores=data["data"]["individualScores"],
            history={game_num: RundownHistoryGame(
                index=game_data["index"],
                game=Game[game_data["game"]],
                multiplier=game_data["multiplier"],
                individualScores=game_data.get("individualScores"),
                gameScores={Team[team]: score for team, score in game_data["gameScores"].items()}
                if "gameScores" in game_data else None,
                eventScores={Team[team]: score for team, score in game_data["eventScores"].items()}
                if "eventScores" in game_data else None,
                gamePlacements={Team[team]: placement for team, placement in game_data["gamePlacements"].items()}
                if "gamePlacements" in game_data else None,
                eventPlacements={Team[team]: placement for team, placement in game_data["eventPlacements"].items()}
                if "eventPlacements" in game_data else None
            ) for game_num, game_data in data["data"]["history"].items()},
            creators={Team[team]: creator for team, creator in data["data"]["creators"].items()}
        )


@dataclass(frozen=True, slots=True)
class Creator:
    """Detailed data for a given participant."""

    username: str
    """The Minecraft username of the participant."""
    uuid: str
    """The Minecraft UUID of the participant."""
    stream: str
    """The streaming URL of the participant."""


class ParticipantsResponse(BaseResponse):
    """Response object representing all teams and their participants in the current event cycle."""

    data: dict[Team, list[Creator]]
    """Dictionary mapping from teams to lists of detailed participant data."""

    def __init__(self: t.Self, request: requests.Response | dict[str, t.Any]) -> None:
        data: dict[str, t.Any] = super()._extract_json_data(request)
        super().__init__(data)

        self.data = {Team[team]: [Creator(
            username=creator["username"],
            uuid=creator["uuid"],
            stream=creator["stream"]
        ) for creator in participants] for team, participants in data["data"].items()}


class ParticipantsTeamResponse(BaseResponse):
    """Response object representing a single team and its participants in the current event cycle."""

    data: list[Creator]
    """List of detailed participant data."""

    def __init__(self: t.Self, request: requests.Response | dict[str, t.Any]) -> None:
        data: dict[str, t.Any] = super()._extract_json_data(request)
        super().__init__(data)

        if self.code == 400:
            raise InvalidTeamError(self.code, self.reason)

        self.data = [
            Creator(
                username=creator["username"],
                uuid=creator["uuid"],
                stream=creator["stream"]
            ) for creator in data["data"]
        ]
