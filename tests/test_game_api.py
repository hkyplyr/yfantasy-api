import requests_mock

from yfantasy_api.api import YahooFantasyApi


def mock_request(requests_mock, path, response_name):
    with open(f'tests/resources/game/{response_name}.json') as f:
        print(YahooFantasyApi.base_url + '/' + path)
        requests_mock.get(f'{YahooFantasyApi.base_url}/{path}', text=f.read())


def test_game_weeks(requests_mock):
    sub_resource = 'game_weeks'
    path = f'game/nhl/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.game().game_weeks().get(), sub_resource)


def test_game_old(requests_mock):
    path = 'game/nhl'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'old')

    hasattr(api.game().get(), 'game_key')


def test_position_types(requests_mock):
    sub_resource = 'position_types'
    path = f'game/nhl/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.game().position_types().get(), sub_resource)


def test_roster_positions(requests_mock):
    sub_resource = 'roster_positions'
    path = f'game/nhl/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.game().roster_positions().get(), sub_resource)


def test_stat_categories(requests_mock):
    sub_resource = 'stat_categories'
    path = f'game/nhl/{sub_resource}'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.game().stat_categories().get(), sub_resource)


def test_games(requests_mock):
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    path = 'games;is_available=1;game_codes=nhl;seasons=2020'
    mock_request(requests_mock, path, 'games')

    api.games().get(is_available=True, game_codes=['nhl'], seasons=[2020])
