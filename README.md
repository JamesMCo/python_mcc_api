# Python MCC API

[![🐍 PyPI](https://img.shields.io/pypi/v/mcc-api?label=🐍%20PyPI)](https://pypi.org/project/mcc-api/)
[![👑 Targeting Event API v1.6.0](https://img.shields.io/badge/👑_Targeting_Event_API-v1.6.0-red)](https://github.com/Noxcrew/mcchampionship-api/releases/tag/v1.6.0)
[![🏝️ Targeting Island API v25.03.13](https://img.shields.io/badge/🏝️_Targeting_Island_API-v25.03.13-aqua)](https://github.com/Noxcrew/mccisland-api/releases/tag/v25.03.13)

A helper library for the [MC Championship](https://mcchampionship.com) APIs
([Event](https://github.com/Noxcrew/mcchampionship-api), inspired by [derNiklaas's](https://github.com/derNiklaas)
[node-mcc-api](https://github.com/derNiklaas/node-mcc-api) project, and
[Island](https://github.com/Noxcrew/mccisland-api)).

- Issues: [https://github.com/JamesMCo/python_mcc_api/issues](https://github.com/JamesMCo/python_mcc_api/issues)
- MCC Event API documentation: [https://api.mcchampionship.com/docs](https://api.mcchampionship.com/docs)
- MCC Island API documentation: [https://api.mccisland.net/docs](https://api.mccisland.net/docs)
- Module documentation: [https://mrjamesco.uk/python_mcc_api](https://mrjamesco.uk/python_mcc_api)
- PyPI: [https://pypi.org/project/mcc-api/](https://pypi.org/project/mcc-api/)
- Repository: [https://github.com/JamesMCo/python_mcc_api](https://github.com/JamesMCo/python_mcc_api)

## Installation

Ensure that [pip](https://packaging.python.org/en/latest/key_projects/#pip) is updated using:

```bash
python -m pip install --upgrade pip
```

Then install or update `mcc_api` using:

```bash
pip install --upgrade mcc-api
```

## Usage

### Event

The event library provides methods to call each of the endpoints described in the MC Championship Event API's
[documentation](https://api.mcchampionship.com/docs).

```python
from datetime import datetime, timezone
from mcc_api.event import get_event, get_rundown

# Print information about the current event cycle

event = get_event()
event_name = event.data.event
event_start = event.data.date.strftime("%I%p UTC on %A %d %B %Y")

if event.data.date <= datetime.now(tz=timezone.utc):
    print(f"The latest event (MCC {event_name}) started at {event_start}.")
else:
    print(f"The upcoming event (MCC {event_name}) starts at {event_start}.")


# Print the names of the players that played in Dodgebolt in the latest event

rundown = get_rundown()

dodgebolt_teams = rundown.data.dodgeboltData.keys()
players = sorted([player for team in dodgebolt_teams for player in rundown.data.creators[team]], key=str.casefold)

print(f"The players that played in Dodgebolt in the latest event were:\n- {'\n- '.join(players)}")
```

### Island

The island library provides an implementation of the GraphQL schema described in the MCC Island API's
[documentation](https://api.mccisland.net/docs). Queries are written in GraphQL, and validated locally before being sent
to the API.

Accessing the MCC Island API requires an API key, which can be minted using
[Noxcrew Gateway](https://gateway.noxcrew.com). Then, you can use `mcc_api.island.set_api_key("<YOUR_API_KEY>")` to
provide authentication for all future requests. It is recommended that you store your API key in an environment
variable, and don't check it in to your source controlled repository.

```python
from gql import gql
from mcc_api.island import client, set_api_key

set_api_key("<YOUR_API_KEY>")

# Print some information about a given player
query = gql("""
    query player($username: String!) {
        playerByUsername(username: $username) {
            username
            status {
                online
            }
            collections {
                currency {
                    coins
                }
            }
            social {
                friends {
                    uuid
                }
            }
        }
    }
""")
data = client.execute(query, variable_values={"username": "Jammy4312"})

player = data["playerByUsername"]
username = player["username"]
username_s = f"{username}'{'' if player['username'][-1].lower() == 's' else 's'}"

print(f"Username: {username}")
if "status" in player:
    print(f"Status:   {'Online' if player['status']['online'] else 'Offline'}")
else:
    print(f"Status:   Unknown ({username_s} status is private)")

if "collections" in player:
    print(f"Coins:    {player['collections']['currency']['coins']:,}")
else:
    print(f"Coins:    Unknown ({username_s} collections are private)")

if "social" in player:
    print(f"Friends:  {len(player['social']['friends']):,}")
else:
    print(f"Friends:  Unknown ({username_s} social data are private)")
```
