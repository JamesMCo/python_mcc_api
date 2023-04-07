import mcc_api
import json
import typing as t
import unittest


class TestEventParticipants200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: mcc_api.ParticipantsResponse

    def setUp(self: t.Self) -> None:
        with open("mock_data/200_participants.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = mcc_api.ParticipantsResponse(self.response_json)

    def test_all_teams_present(self: t.Self) -> None:
        for team in mcc_api.Team:
            with self.subTest(team=str(team)):
                self.assertIn(team, self.response_object.data)

    def test_all_participants_unique(self: t.Self) -> None:
        participants_count: int = 0
        usernames: set[str] = set()
        uuids: set[str] = set()

        for _, participants in self.response_object.data.items():
            participants: list[mcc_api.responses.Creator]
            for participant in participants:
                participant: mcc_api.responses.Creator

                participants_count += 1
                usernames.add(participant.username)
                uuids.add(participant.uuid)

        self.assertEqual(participants_count, len(usernames))
        self.assertEqual(participants_count, len(uuids))


class TestParticipantsEndpoint429(unittest.TestCase):
    def test_participants_ratelimit_exception(self: t.Self) -> None:
        with open("mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.RateLimitError, mcc_api.ParticipantsResponse, response_json)


class TestEventParticipantsTeam200(unittest.TestCase):
    response_json: dict[str, t.Any]
    response_object: mcc_api.ParticipantsTeamResponse

    def setUp(self: t.Self) -> None:
        with open("mock_data/200_participants_team.json") as f:
            f: t.TextIO
            self.response_json = json.loads(f.read())
        self.response_object = mcc_api.ParticipantsTeamResponse(self.response_json)

    def test_all_participants_unique(self: t.Self) -> None:
        participants_count: int = 0
        usernames: set[str] = set()
        uuids: set[str] = set()

        for participant in self.response_object.data:
            participant: mcc_api.responses.Creator

            participants_count += 1
            usernames.add(participant.username)
            uuids.add(participant.uuid)

        self.assertEqual(participants_count, len(usernames))
        self.assertEqual(participants_count, len(uuids))


class TestParticipantsTeamEndpoint400(unittest.TestCase):
    def test_participants_team_invalid_team_exception(self: t.Self) -> None:
        with open("mock_data/400_participants_team.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.InvalidTeamError, mcc_api.ParticipantsTeamResponse, response_json)


class TestParticipantsTeamEndpoint429(unittest.TestCase):
    def test_participants_team_ratelimit_exception(self: t.Self) -> None:
        with open("mock_data/429_ratelimit.json") as f:
            f: t.TextIO
            response_json: dict[str, t.Any] = json.loads(f.read())
        self.assertRaises(mcc_api.exceptions.RateLimitError, mcc_api.ParticipantsTeamResponse, response_json)


if __name__ == "__main__":
    unittest.main()
