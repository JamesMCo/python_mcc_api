import graphql
from mcc_api import __user_agent as mcc_api_user_agent
import mcc_api.island
import requests
import unittest


class TestIslandSchemaMatches(unittest.TestCase):
    def test_schema_matches(self: "TestIslandSchemaMatches") -> None:
        schema_request: requests.Response = requests.get(
            "https://api.mccisland.net/graphql/schema",
            headers={"User-Agent": mcc_api_user_agent}
        )

        if schema_request.status_code != 200:
            self.fail(f"Unable to retrieve MCC Island API schema: {schema_request.status_code} {schema_request.reason}")
        online_schema: graphql.GraphQLSchema = graphql.build_schema(schema_request.text)

        changes = graphql.find_breaking_changes(online_schema, mcc_api.island.schema) +\
                  graphql.find_dangerous_changes(online_schema, mcc_api.island.schema)

        self.assertEqual(
            len(changes), 0,
            "Changes in schema found:\n" + "\n".join(f"{change.type.name}: {change.description}" for change in changes)
        )


if __name__ == "__main__":
    unittest.main()
