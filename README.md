# Yahoo Fantasy API
> A simply Python client that can be used to make calls to the Yahoo! Fantasy Sports API.

![Python package](https://github.com/hkyplyr/yfantasy-api/workflows/Python%20package/badge.svg)

This library provides a fluent API to build and make calls to the Yahoo! Fantasy Sports API. It was developed specifically for NHL use initially, but should be generic enough to support MLB, NBA, and NFL as well.

## Installation
``` sh
pip install yfantasy_api
```

## Usage examples
### Obtain team information, including the roster with player stats for March 31st 2021
``` python
# The request url created is: /team/nhl.l.12345.t.1/roster/players/stats;type=date;date=2021-03-31
from yfantasy_api.api import YahooFantasyApi

league_id = 12345  # This should be the id of the league you are querying
game_id = 'nhl'    # This should be the id of the game you are querying
team_id = 1        # This should be the id of the team you are querying

api = YahooFantasyApi(league_id, game_id)
team = api \
    .team(team_id) \
    .roster() \
    .stats(date='2021-03-31') \
    .get()

for player in team.players:
    print(player.full_name, player.points)

# Output:
# Brock Nelson 0.00
# Joel Eriksson Ek 0.05
# Nazem Kadri 4.00
# Alex Ovechkin 0.00
# Jake Guentzel 0.00
# ...truncated for brevity...
```

### Obtain draft_results, including player information for each pick.
``` python
# The request url created is: /league/nhl.l.12345/draft_results/players
from yfantasy_api.api import YahooFantasyApi

league_id = 12345  # This should be the id of the league you are querying
game_id = 'nhl'    # This should be the id of the game you are querying
team_id = 1        # This should be the id of the team you are querying

api = YahooFantasyApi(league_id, game_id)
league = api \
    .league() \
    .draft_results() \
    .players() \
    .get()

for draft_result in league.draft_results:
    print(f'{draft_result.round} - {draft_result.pick} - {draft_result.player.full_name}')

# Output:
# 1 - 1 - Connor McDavid
# 1 - 2 - Alex Ovechkin
# 1 - 3 - Patrick Kane
# 1 - 4 - Steven Stamkos
# 1 - 5 - Sidney Crosby
# ...truncated for brevity...
```
For working examples of the above scenarios, see [examples.py](examples.py)

## Development setup
I suggest you use some form of virtual environment to avoid clashing dependencies, but that is obviously your call. My suggested virtual environment is [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).
``` sh
git clone git@github.com:hkyplyr/yfantasy-api.git
...
cd yfantasy_api
...
pip install -r requirements.txt
```

## Release History
TODO

## Meta
Travis Paquette - [@hkyplyr](https://twitter.com/hkyplyr) - tpaqu15@gmail.com  
Distributed under the MIT license. See [`LICENSE`](LICENSE) for more information.
## How to Contribute
1. Clone repo and create a new branch: $ git checkout -b short_feature_name.
2. Make changes and test
3. Submit a Pull Request