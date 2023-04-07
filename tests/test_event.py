from datetime import datetime, timezone
import mcc_api
import json
import typing as t
import unittest


class TestEventEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: mcc_api.EventInformationResponse

    def setUp(self: t.Self) -> None:
        with open("mock_data/200_event.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = mcc_api.EventInformationResponse(self.response_json)

    def test_date(self: t.Self) -> None:
        self.assertEqual(self.response_object.data.date, datetime(2023, 4, 2, 1, 13, 3, 587000, timezone.utc))

    def test_event_name(self: t.Self) -> None:
        self.assertEqual(self.response_object.data.event, "22")

    def test_update_video(self: t.Self) -> None:
        self.assertEqual(self.response_object.data.updateVideo, "https://www.youtube.com/embed/LdelXw4FsAE")


class TestEventEndpoint429(unittest.TestCase):
    def test_event_ratelimit_exception(self: t.Self) -> None:
        with open("mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.RateLimitError, mcc_api.EventInformationResponse, response_json)


if __name__ == "__main__":
    unittest.main()
