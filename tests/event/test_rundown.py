import mcc_api.event as event_api
import json
import typing as t
import unittest


class TestRundownEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.RundownResponse

    def setUp(self: "TestRundownEndpoint200") -> None:
        with open("event/mock_data/200_rundown.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.RundownResponse(self.response_json)

    def test_dodgebolt(self: "TestRundownEndpoint200") -> None:
        self.assertEqual(len(self.response_object.data.dodgeboltData), 2)

        team_one: event_api.Team
        team_two: event_api.Team
        team_one, team_two = self.response_object.data.dodgeboltData.keys()

        self.assertNotEqual(team_one, team_two)
        self.assertNotEqual(
            self.response_object.data.dodgeboltData[team_one],
            self.response_object.data.dodgeboltData[team_two]
        )

    def test_event_placements_and_scores_match(self: "TestRundownEndpoint200") -> None:
        placements: list[event_api.Team] = sorted(
            self.response_object.data.eventPlacements.keys(),
            key=lambda team: self.response_object.data.eventPlacements[team],
            reverse=True
        )
        scores: list[event_api.Team] = sorted(
            self.response_object.data.eventScores.keys(),
            key=lambda team: self.response_object.data.eventScores[team]
        )
        self.assertEqual(placements, scores)

    def test_event_individual_scores_contain_all_participants(self: "TestRundownEndpoint200") -> None:
        participant_teams: list[event_api.Team] = [
            event_api.Team.RED,
            event_api.Team.ORANGE,
            event_api.Team.YELLOW,
            event_api.Team.LIME,
            event_api.Team.GREEN,
            event_api.Team.CYAN,
            event_api.Team.AQUA,
            event_api.Team.BLUE,
            event_api.Team.PURPLE,
            event_api.Team.PINK
        ]
        participants: list[str] = [
            participant
            for team in participant_teams
            for participant in self.response_object.data.creators[team]
        ]
        self.assertEqual(
            sorted(self.response_object.data.individualScores, key=str.casefold),
            sorted(participants, key=str.casefold)
        )

    def test_history_contains_eight_games(self: "TestRundownEndpoint200") -> None:
        self.assertEqual(len(self.response_object.data.history), 8)

    def test_history_multipliers(self: "TestRundownEndpoint200") -> None:
        for game, multiplier in zip(range(8), [1, 1.5, 1.5, 2, 2, 2.5, 2.5, 3]):
            with self.subTest(game=game):
                self.assertEqual(self.response_object.data.history[str(game)].multiplier, multiplier)


class TestRundownEndpoint404(unittest.TestCase):
    def test_rundown_invalid_event_exception(self: "TestRundownEndpoint404") -> None:
        with open("event/mock_data/404_rundown.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.InvalidEventError, event_api.RundownResponse, response_json)


class TestRundownEndpoint429(unittest.TestCase):
    def test_rundown_ratelimit_exception(self: "TestRundownEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.RundownResponse, response_json)


if __name__ == "__main__":
    unittest.main()
