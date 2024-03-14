from datetime import datetime, timezone
import mcc_api.event as event_api
import json
import typing as t
import unittest


class TestEventEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.EventInformationResponse

    def setUp(self: "TestEventEndpoint200") -> None:
        with open("event/mock_data/200_event.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.EventInformationResponse(self.response_json)

    def test_date(self: "TestEventEndpoint200") -> None:
        self.assertEqual(self.response_object.data.date, datetime(2023, 4, 2, 1, 13, 3, 587000, timezone.utc))

    def test_event_name(self: "TestEventEndpoint200") -> None:
        self.assertEqual(self.response_object.data.event, "22")

    def test_update_video(self: "TestEventEndpoint200") -> None:
        self.assertEqual(self.response_object.data.updateVideo, "https://www.youtube.com/embed/LdelXw4FsAE")


class TestEventEndpoint429(unittest.TestCase):
    def test_event_ratelimit_exception(self: "TestEventEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.EventInformationResponse, response_json)


if __name__ == "__main__":
    unittest.main()
