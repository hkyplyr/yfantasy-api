import requests_mock

from pytest import raises
from yfantasy_api.api import YahooFantasyApi


def mock_request(requests_mock, path, response_name):
    with open(f'tests/resources/league/{response_name}.json') as f:
        requests_mock.get(f'{YahooFantasyApi.base_url}/{path}', text=f.read())


def test_draft_results(requests_mock):
    sub_resource = 'draftresults'
    path = f'league/nhl.l.123456/{sub_resource}/players'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().draft_results().get(), sub_resource)


def test_meta(requests_mock):
    path = 'league/nhl.l.123456'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'meta')

    hasattr(api.league().meta().get(), 'league_id')


def test_players(requests_mock):
    sub_resource = 'players'
    path = f'league/nhl.l.123456/{sub_resource};search=search;status=K'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().players(search='search', status='K').get(), sub_resource)

def test_players_empty(requests_mock):
    path = f'league/nhl.l.123456/players;search=search;status=K'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, "players_empty")

    hasattr(api.league().players(search='search', status='K').get(), 'players')

def test_players_with_draft_analysis(requests_mock):
    path = 'league/nhl.l.123456/players;start=0;count=25/draft_analysis'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'players_with_draft_analysis')

    hasattr(api.league().players().draft_analysis().get(), 'players')


def test_players_with_ownership(requests_mock):
    path = 'league/nhl.l.123456/players;start=0;count=25/ownership'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'players_with_ownership')

    hasattr(api.league().players().ownership().get(), 'players')


def test_players_with_percent_owned(requests_mock):
    path = 'league/nhl.l.123456/players;start=0;count=25/percent_owned'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'players_with_percent_owned')

    hasattr(api.league().players().percent_owned().get(), 'players')


def test_players_with_stats(requests_mock):
    path = 'league/nhl.l.123456/players;start=0;count=25/stats'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'players_with_stats')

    hasattr(api.league().players().stats().get(), 'players')


def test_players_with_stats_filter_date(requests_mock):
    path = 'league/nhl.l.123456/players;start=0;count=25/stats;date=2021-03-01'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'players_with_stats')

    hasattr(api.league().players().stats(date='2021-03-01').get(), 'players')


def test_players_with_stats_filter_season(requests_mock):
    path = 'league/nhl.l.123456/players;start=0;count=25/stats;season=2021'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'players_with_stats')

    hasattr(api.league().players().stats(season=2021).get(), 'players')


def test_players_with_stats_filter_week(requests_mock):
    path = 'league/nhl.l.123456/players;start=0;count=25/stats;week=1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'players_with_stats')

    hasattr(api.league().players().stats(week=1).get(), 'players')


def test_players_with_stats_more_than_one_coverage(requests_mock):
    api = YahooFantasyApi(123456, 'nhl', timeout=0)

    with raises(Exception) as sys_exit_e:
        api.league().players().stats(date='2021-03-01', season=2020).get()
    assert sys_exit_e.type == Exception


def test_scoreboard(requests_mock):
    sub_resource = 'scoreboard'
    path = f'league/nhl.l.123456/{sub_resource};week=1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().scoreboard(week=1).get(), sub_resource)


def test_scoreboard_nfl(requests_mock):
    sub_resource = 'scoreboard'
    path = f'league/nhl.l.123456/{sub_resource};week=1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'scoreboard_nfl')

    hasattr(api.league().scoreboard(week=1).get(), sub_resource)


def test_settings(requests_mock):
    sub_resource = 'settings'
    path = f'league/nhl.l.123456/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().settings().get(), sub_resource)


def test_settings_nfl(requests_mock):
    sub_resource = 'settings'
    path = f'league/nhl.l.123456/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'settings_nfl')

    hasattr(api.league().settings().get(), sub_resource)



def test_standings(requests_mock):
    sub_resource = 'standings'
    path = f'league/nhl.l.123456/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().standings().get(), sub_resource)


def test_teams(requests_mock):
    sub_resource = 'teams'
    path = f'league/nhl.l.123456/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().teams().get(), sub_resource)


def test_transactions(requests_mock):
    sub_resource = 'transactions'
    path = f'league/nhl.l.123456/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().transactions().get(), sub_resource)


def test_transactions_empty(requests_mock):
    sub_resource = 'transactions'
    path = f'league/nhl.l.123456/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'transactions_empty')

    hasattr(api.league().transactions().get(), sub_resource)


def test_transactions_waiver_missing_team():
    api = YahooFantasyApi(123456, 'nhl', timeout=0)

    with raises(Exception) as sys_exit_e:
        api.league().transactions(ttype='waiver').get()
    assert sys_exit_e.type == Exception


def test_transactions_waiver(requests_mock):
    sub_resource = 'transactions'
    path = f'league/nhl.l.123456/{sub_resource};type=waiver;team_key=nhl.l.123456.t.1;count=1;start=1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.league().transactions(ttype='waiver', team_id=1, count=1, start=1).get(), sub_resource)
