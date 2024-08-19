import mcc_api.event as event_api
import json
import typing as t
import unittest


class TestEventParticipant200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.ParticipantResponse

    def setUp(self: "TestEventParticipant200") -> None:
        with open("event/mock_data/200_participant.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.ParticipantResponse(self.response_json)

    def test_creator_returned(self: "TestEventParticipant200") -> None:
        self.assertIsInstance(self.response_object.data, event_api.responses.Creator)


class TestParticipantEndpoint404(unittest.TestCase):
    def test_participant_invalid_team_exception(self: "TestParticipantEndpoint404") -> None:
        with open("event/mock_data/404_participant.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.InvalidParticipantError, event_api.ParticipantResponse, response_json)


class TestParticipantEndpoint429(unittest.TestCase):
    def test_participant_ratelimit_exception(self: "TestParticipantEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.ParticipantResponse, response_json)


class TestEventParticipants200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.ParticipantsResponse

    def setUp(self: "TestEventParticipants200") -> None:
        with open("event/mock_data/200_participants.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.ParticipantsResponse(self.response_json)

    def test_all_teams_present(self: "TestEventParticipants200") -> None:
        for team in event_api.Team:
            with self.subTest(team=str(team)):
                self.assertIn(team, self.response_object.data)

    def test_all_participants_unique(self: "TestEventParticipants200") -> None:
        participants_count: int = 0
        usernames: set[str] = set()
        uuids: set[str] = set()

        for _, participants in self.response_object.data.items():
            participants: list[event_api.responses.Creator]
            for participant in participants:
                participant: event_api.responses.Creator

                participants_count += 1
                usernames.add(participant.username)
                uuids.add(participant.uuid)

        self.assertEqual(participants_count, len(usernames))
        self.assertEqual(participants_count, len(uuids))


class TestParticipantsEndpoint429(unittest.TestCase):
    def test_participants_ratelimit_exception(self: "TestParticipantsEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.ParticipantsResponse, response_json)


class TestEventParticipantsTeam200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: event_api.ParticipantsTeamResponse

    def setUp(self: "TestEventParticipantsTeam200") -> None:
        with open("event/mock_data/200_participants_team.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = event_api.ParticipantsTeamResponse(self.response_json)

    def test_all_participants_unique(self: "TestEventParticipantsTeam200") -> None:
        participants_count: int = 0
        usernames: set[str] = set()
        uuids: set[str] = set()

        for participant in self.response_object.data:
            participant: event_api.responses.Creator

            participants_count += 1
            usernames.add(participant.username)
            uuids.add(participant.uuid)

        self.assertEqual(participants_count, len(usernames))
        self.assertEqual(participants_count, len(uuids))


class TestParticipantsTeamEndpoint404(unittest.TestCase):
    def test_participants_team_invalid_team_exception(self: "TestParticipantsTeamEndpoint404") -> None:
        with open("event/mock_data/404_participants_team.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.InvalidTeamError, event_api.ParticipantsTeamResponse, response_json)


class TestParticipantsTeamEndpoint429(unittest.TestCase):
    def test_participants_team_ratelimit_exception(self: "TestParticipantsTeamEndpoint429") -> None:
        with open("event/mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(event_api.exceptions.RateLimitError, event_api.ParticipantsTeamResponse, response_json)


if __name__ == "__main__":
    unittest.main()
