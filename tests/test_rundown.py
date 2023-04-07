import mcc_api
import json
import typing as t
import unittest


class TestRundownEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: mcc_api.RundownResponse

    def setUp(self: t.Self) -> None:
        with open("mock_data/200_rundown.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = mcc_api.RundownResponse(self.response_json)

    def test_dodgebolt(self: t.Self) -> None:
        self.assertEqual(len(self.response_object.data.dodgeboltData), 2)

        team_one: mcc_api.Team
        team_two: mcc_api.Team
        team_one, team_two = self.response_object.data.dodgeboltData.keys()

        self.assertNotEqual(team_one, team_two)
        self.assertNotEqual(
            self.response_object.data.dodgeboltData[team_one],
            self.response_object.data.dodgeboltData[team_two]
        )

    def test_event_placements_and_scores_match(self: t.Self) -> None:
        placements: list[mcc_api.Team] = sorted(
            self.response_object.data.eventPlacements.keys(),
            key=lambda team: self.response_object.data.eventPlacements[team],
            reverse=True
        )
        scores: list[mcc_api.Team] = sorted(
            self.response_object.data.eventScores.keys(),
            key=lambda team: self.response_object.data.eventScores[team]
        )
        self.assertEqual(placements, scores)

    def test_event_individual_scores_contain_all_participants(self: t.Self) -> None:
        participant_teams: list[mcc_api.Team] = [
            mcc_api.Team.RED,
            mcc_api.Team.ORANGE,
            mcc_api.Team.YELLOW,
            mcc_api.Team.LIME,
            mcc_api.Team.GREEN,
            mcc_api.Team.CYAN,
            mcc_api.Team.AQUA,
            mcc_api.Team.BLUE,
            mcc_api.Team.PURPLE,
            mcc_api.Team.PINK
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

    def test_history_contains_eight_games(self: t.Self) -> None:
        self.assertEqual(len(self.response_object.data.history), 8)

    def test_history_multipliers(self: t.Self) -> None:
        for game, multiplier in zip(range(8), [1, 1.5, 1.5, 2, 2, 2.5, 2.5, 3]):
            with self.subTest(game=game):
                self.assertEqual(self.response_object.data.history[str(game)].multiplier, multiplier)


class TestRundownEndpoint400(unittest.TestCase):
    def test_rundown_invalid_event_exception(self: t.Self) -> None:
        with open("mock_data/400_rundown.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.InvalidEventError, mcc_api.RundownResponse, response_json)


class TestRundownEndpoint429(unittest.TestCase):
    def test_rundown_ratelimit_exception(self: t.Self) -> None:
        with open("mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.RateLimitError, mcc_api.RundownResponse, response_json)


if __name__ == "__main__":
    unittest.main()
