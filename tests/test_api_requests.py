from pytest import fixture
from pytest_mock import mocker

from yfantasy_api.api import YahooFantasyApi
from yfantasy_api.auth import AuthenticationService


@fixture(autouse=True)
def setup(mocker):
    mocker.patch.object(AuthenticationService, '_AuthenticationService__cache_tokens').return_val = None
    mocker.patch.object(AuthenticationService, '_AuthenticationService__set_tokens').return_val = None
    mocker.patch.object(YahooFantasyApi, '_YahooFantasyApi__set_tokens').return_val = None
    mocker.patch.object(YahooFantasyApi, '_YahooFantasyApi__get_resource').return_val = (None, None)


def test_get_user_teams():
    yfs = YahooFantasyApi(123456)
    yfs.get_user_teams()

    path = 'users;use_login=1/teams'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_game_weeks():
    yfs = YahooFantasyApi(123456)
    yfs.get_game_weeks()

    path = 'game/nhl/game_weeks'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_stat_categories():
    yfs = YahooFantasyApi(123456)
    yfs.get_stat_categories()

    path = 'game/nhl/stat_categories'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_position_types():
    yfs = YahooFantasyApi(123456)
    yfs.get_position_types()

    path = 'game/nhl/position_types'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_roster_positions():
    yfs = YahooFantasyApi(123456)
    yfs.get_roster_positions()

    path = 'game/nhl/roster_positions'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_settings():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_settings()

    path = 'league/nhl.l.123456/settings'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_standings():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_standings()

    path = 'league/nhl.l.123456/standings'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_scoreboard():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_scoreboard(1)

    path = 'league/nhl.l.123456/scoreboard;week=1'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_teams():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_teams()

    path = 'league/nhl.l.123456/teams'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_roster():
    yfs = YahooFantasyApi(123456)
    yfs.get_roster(1)

    path = 'team/nhl.l.123456.t.1/roster'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_players():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_players(0)

    path = 'league/nhl.l.123456/players;start=0;type=season/ownership'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_keepers():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_keepers(0)

    path = 'league/nhl.l.123456/players;start=0;status=K'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_draft_results():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_draft_results()

    path = 'league/nhl.l.123456/draftresults'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_leage_transactions():
    yfs = YahooFantasyApi(123456)
    yfs.get_leage_transactions()

    path = 'league/nhl.l.123456/transactions'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_team_matchups():
    yfs = YahooFantasyApi(123456)
    yfs.get_team_matchups(1, [1, 2, 3])

    path = 'team/nhl.l.123456.t.1/matchups;weeks1,2,3'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_team_stats_date():
    yfs = YahooFantasyApi(123456)
    yfs.get_team_stats(1, 'date', None)

    path = 'team/nhl.l.123456.t.1/roster;type=date;date=date/players/stats'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_team_stats_week():
    yfs = YahooFantasyApi(123456)
    yfs.get_team_stats(1, None, 'week')

    path = 'team/nhl.l.123456.t.1/roster;type=week;week=week/players/stats'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_team_stats_neither():
    yfs = YahooFantasyApi(123456)
    yfs.get_team_stats(1, None, None)

    yfs._YahooFantasyApi__get_resource.assert_not_called()


def test_get_league_player_ownership():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_player_ownership(0)

    path = 'league/nhl.l.123456/players;start=0;type=season/ownership'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_league_player_stats():
    yfs = YahooFantasyApi(123456)
    yfs.get_league_player_stats(0, 'date')

    path = 'league/nhl.l.123456/players;start=0;out=ownership/stats;type=date;date=date'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)


def test_get_stats_players_season():
    yfs = YahooFantasyApi(123456)
    yfs.get_stats_players_season(0)

    path = 'league/nhl.l.123456/players;start=0;sort=AR/stats;type=season;season=2020'
    yfs._YahooFantasyApi__get_resource.assert_called_with(path)
