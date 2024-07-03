import mcc_api.event as event_api
import json
import typing as t
import unittest


class TestEventsEndpoint200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.EventsResponse

    def setUp(self: "TestEventsEndpoint200") -> None:
        with open("event/mock_data/200_events.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.EventsResponse(self.response_json)

    def test_all_numbered_events_present(self: "TestEventsEndpoint200") -> None:
        for event_number in range(1, 36):
            with self.subTest(event=event_number):
                self.assertIn(str(event_number), self.response_object.data)

    def test_all_named_events_present(self: "TestEventsEndpoint200") -> None:
        for event_number in ["AF", "P23", "R2", "TR", "PARTY", "4KO", "P24", "TRE"]:
            with self.subTest(event=event_number):
                self.assertIn(str(event_number), self.response_object.data)


class TestEventsEndpoint429(unittest.TestCase):
    def test_event_ratelimit_exception(self: "TestEventsEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.EventsResponse, response_json)


if __name__ == "__main__":
    unittest.main()
