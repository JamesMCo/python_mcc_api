import mcc_api.event as event_api
import json
import typing as t
import unittest


class TestHallOfFameEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.HallOfFameResponse

    def setUp(self: "TestHallOfFameEndpoint200") -> None:
        with open("event/mock_data/200_halloffame.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.HallOfFameResponse(self.response_json)

    def test_game_names(self: "TestHallOfFameEndpoint200") -> None:
        self.assertIn(event_api.Game.GLOBAL_STATISTICS, self.response_object.data)
        self.assertIn(event_api.Game.LEGACY_STATISTICS, self.response_object.data)

    def test_records(self: "TestHallOfFameEndpoint200") -> None:
        for game in [event_api.Game.GLOBAL_STATISTICS, event_api.Game.LEGACY_STATISTICS]:
            with self.subTest(game=str(game)):
                self.assertIn(
                    game,
                    self.response_object.data
                )

                records: dict[str, event_api.responses.HallOfFameRecord] = self.response_object.data[game]

                self.assertIn("RECORD NAME 1", records)
                self.assertEqual(records["RECORD NAME 1"].placement, 0)
                self.assertEqual(records["RECORD NAME 1"].player, "MCChampionship")
                self.assertEqual(records["RECORD NAME 1"].value, "String value")
                self.assertFalse(records["RECORD NAME 1"].changedHands)

                self.assertIn("RECORD NAME 2", records)
                self.assertEqual(records["RECORD NAME 2"].placement, 1)
                self.assertEqual(records["RECORD NAME 2"].player, "MCChampionship")
                self.assertEqual(records["RECORD NAME 2"].value, 0)
                self.assertTrue(records["RECORD NAME 2"].changedHands)


class TestHallOfFameEndpoint429(unittest.TestCase):
    response_json: dict[str, t.Any]

    def test_halloffame_ratelimit_exception(self: "TestHallOfFameEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.HallOfFameResponse, response_json)


class TestHallOfFameGameEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.HallOfFameGameResponse

    def setUp(self: "TestHallOfFameGameEndpoint200") -> None:
        with open("event/mock_data/200_halloffame_game.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.HallOfFameGameResponse(self.response_json)

    def test_records(self: "TestHallOfFameGameEndpoint200") -> None:
        records: dict[str, event_api.responses.HallOfFameRecord] = self.response_object.data

        self.assertIn("RECORD NAME 1", records)
        self.assertEqual(records["RECORD NAME 1"].placement, 0)
        self.assertEqual(records["RECORD NAME 1"].player, "MCChampionship")
        self.assertEqual(records["RECORD NAME 1"].value, "String value")
        self.assertFalse(records["RECORD NAME 1"].changedHands)

        self.assertIn("RECORD NAME 2", records)
        self.assertEqual(records["RECORD NAME 2"].placement, 1)
        self.assertEqual(records["RECORD NAME 2"].player, "MCChampionship")
        self.assertEqual(records["RECORD NAME 2"].value, 0)
        self.assertTrue(records["RECORD NAME 2"].changedHands)


class TestHallOfFameGameEndpoint404(unittest.TestCase):
    def test_halloffame_game_invalid_game_exception(self: "TestHallOfFameGameEndpoint404") -> None:
        with open("event/mock_data/404_halloffame_game.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.InvalidGameError, event_api.HallOfFameGameResponse, response_json)


class TestHallOfFameGameEndpoint429(unittest.TestCase):
    def test_halloffame_game_ratelimit_exception(self: "TestHallOfFameGameEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.HallOfFameGameResponse, response_json)


if __name__ == "__main__":
    unittest.main()
