import requests_mock

from pytest import raises
from yfantasy_api.api import YahooFantasyApi


def mock_request(requests_mock, path, response_name):
    with open(f'tests/resources/user/{response_name}.json') as f:
        requests_mock.get(f'{YahooFantasyApi.base_url}/{path}', text=f.read())


def test_meta(requests_mock):
    path = 'users;user_login=1'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, 'meta')

    hasattr(api.user().meta().get(), 'guid')


def test_games(requests_mock):
    sub_resource = 'games'
    path = 'users;use_login=1/games'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.user().games().get(), sub_resource)


def test_teams(requests_mock):
    sub_resource = 'teams'
    path = 'users;use_login=1/teams'
    api = YahooFantasyApi(123456, 'nhl', timeout=0)
    mock_request(requests_mock, path, sub_resource)

    hasattr(api.user().teams().get(), sub_resource)

