import requests_mock

from pytest import raises
from yfantasy_api.api import YahooFantasyApi


def mock_request(requests_mock, path, response_name):
    with open(f'tests/resources/team/{response_name}.json') as f:
        requests_mock.get(f'{YahooFantasyApi.base_url}/{path}', text=f.read())


def test_meta(requests_mock):
    path = 'team/nhl.l.123456.t.1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'meta')

    hasattr(api.team(1).meta().get(), 'info')


def test_matchups(requests_mock):
    sub_resource = 'matchups'
    path = f'team/nhl.l.123456.t.1/{sub_resource};weeks=1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.team(1).matchups(week=1).get(), sub_resource)


def test_roster(requests_mock):
    sub_resource = 'roster'
    path = f'team/nhl.l.123456.t.1/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.team(1).roster().get(), sub_resource)


def test_roster_week(requests_mock):
    sub_resource = 'roster'
    path = f'team/nhl.l.123456.t.1/{sub_resource};week=1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.team(1).roster(week=1).get(), sub_resource)


def test_roster_date(requests_mock):
    sub_resource = 'roster'
    path = f'team/nhl.l.123456.t.1/{sub_resource};date=2021-03-01'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.team(1).roster(date='2021-03-01').get(), sub_resource)


def test_roster_with_more_than_one_coverage(requests_mock):
    api = YahooFantasyApi(123456, 'nhl', timeout=0)

    with raises(Exception) as sys_exit_e:
        api.team(1).roster(date='2021-03-01', week=1).get()
    assert sys_exit_e.type == Exception


def test_standings(requests_mock):
    sub_resource = 'standings'
    path = f'team/nhl.l.123456.t.1/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.team(1).standings().get(), sub_resource)


def test_standings_with_divisions(requests_mock):
    sub_resource = 'standings'
    path = f'team/nhl.l.123456.t.1/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'standings_with_divisions')

    hasattr(api.team(1).standings().get(), sub_resource)


def test_stats(requests_mock):
    sub_resource = 'stats'
    path = f'team/nhl.l.123456.t.1/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.team(1).stats().get(), sub_resource)


def test_roster_with_stats(requests_mock):
    sub_resource = 'roster'
    path = f'team/nhl.l.123456.t.1/{sub_resource}/players/stats'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'roster_with_stats')

    hasattr(api.team(1).roster().stats().get(), 'roster')


def test_roster_with_stats_week(requests_mock):
    sub_resource = 'roster'
    path = f'team/nhl.l.123456.t.1/{sub_resource};week=1/players/stats'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'roster_with_stats')

    hasattr(api.team(1).roster(week=1).stats().get(), 'roster')


def test_roster_with_stats_date(requests_mock):
    sub_resource = 'roster'
    path = f'team/nhl.l.123456.t.1/{sub_resource};date=2021-03-01/players/stats'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'roster_with_stats')

    hasattr(api.team(1).roster(date='2021-03-01').stats().get(), 'roster')



