# Python MCC API

A wrapper for the [MC Championship API](https://api.mcchampionship.com), inspired by [derNiklaas's](https://github.com/derNiklaas) [node-mcc-api](https://github.com/derNiklaas/node-mcc-api) project.

- Issues: [https://github.com/JamesMCo/python_mcc_api/issues](https://github.com/JamesMCo/python_mcc_api/issues)
- MCC API documentation: [https://api.mcchampionship.com/docs](https://api.mcchampionship.com/docs)
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

```python
import mcc_api

# Print information about the current event cycle
from datetime import datetime, timezone
event = mcc_api.get_event()
if event.data.date <= datetime.now(tz=timezone.utc):
    print(f"The latest event (MCC {event.data.event}) started at {event.data.date.strftime('%I%p UTC on %A %d %B %Y')}.")
else:
    print(f"The upcoming event (MCC {event.data.event}) starts at {event.data.date.strftime('%I%p UTC on %A %d %B %Y')}.")

# Print the names of the players that played in Dodgebolt in the latest event
rundown = mcc_api.get_rundown()
dodgebolt_teams = rundown.data.dodgeboltData.keys()
players = sorted([player for team in dodgebolt_teams for player in rundown.data.creators[team]], key=str.casefold)
print(f"The players that played in Dodgebolt in the latest event were {', and '.join([', '.join(players[:-1]), players[-1]])}.")
```
