import mcc_api
import json
import typing as t
import unittest


class TestHallOfFameEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: mcc_api.HallOfFameResponse

    def setUp(self: t.Self) -> None:
        with open("mock_data/200_halloffame.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = mcc_api.HallOfFameResponse(self.response_json)

    def test_game_names(self: t.Self) -> None:
        self.assertIn(mcc_api.Game.GLOBAL_STATISTICS, self.response_object.data)
        self.assertIn(mcc_api.Game.LEGACY_STATISTICS, self.response_object.data)

    def test_records(self: t.Self) -> None:
        for game in [mcc_api.Game.GLOBAL_STATISTICS, mcc_api.Game.LEGACY_STATISTICS]:
            with self.subTest(game=str(game)):
                self.assertIn(
                    game,
                    self.response_object.data
                )

                records: dict[str, mcc_api.responses.HallOfFameRecord] = self.response_object.data[game]

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

    def test_halloffame_ratelimit_exception(self: t.Self) -> None:
        with open("mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.RateLimitError, mcc_api.HallOfFameResponse, response_json)


class TestHallOfFameGameEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: mcc_api.HallOfFameGameResponse

    def setUp(self: t.Self) -> None:
        with open("mock_data/200_halloffame_game.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = mcc_api.HallOfFameGameResponse(self.response_json)

    def test_records(self: t.Self) -> None:
        records: dict[str, mcc_api.responses.HallOfFameRecord] = self.response_object.data

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


class TestHallOfFameGameEndpoint400(unittest.TestCase):
    def test_halloffame_game_invalid_game_exception(self: t.Self) -> None:
        with open("mock_data/400_halloffame_game.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.InvalidGameError, mcc_api.HallOfFameGameResponse, response_json)


class TestHallOfFameGameEndpoint429(unittest.TestCase):
    def test_halloffame_game_ratelimit_exception(self: t.Self) -> None:
        with open("mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.RateLimitError, mcc_api.HallOfFameGameResponse, response_json)


if __name__ == "__main__":
    unittest.main()
