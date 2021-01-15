import json
import requests_mock
import time

from pytest import fixture, raises
from pytest_mock import mocker

from yfantasy_api.api import YahooFantasyApi, BASE_URL
from yfantasy_api.auth import AuthenticationService


@fixture(autouse=True)
def setup(mocker):
    mocker.patch.object(AuthenticationService, '_AuthenticationService__cache_tokens').return_val = None
    mocker.patch.object(AuthenticationService, '_AuthenticationService__set_tokens').return_val = None
    mocker.patch.object(AuthenticationService, 'get_access_token').return_val = 'access_token'
    mocker.patch.object(AuthenticationService, 'get_expires_by').return_val = 'expires_by'
    mocker.patch.object(AuthenticationService, 'get_refresh_token').return_val = 'refresh_token'
    mocker.patch.object(AuthenticationService, 'refresh_tokens').return_val = None


def get_response_stub():
    with open('tests/resources/api_response_stub.json') as f:
        return f.read()


def test_get_resource_valid_tokens(requests_mock):
    requests_mock.get(f'{BASE_URL}/game/nhl/game_weeks', text=get_response_stub())

    yfs, _ = make_api_call(is_valid=True)

    yfs.auth_service.refresh_tokens.assert_not_called()


def test_get_resource_invalid_tokens(requests_mock):
    requests_mock.get(f'{BASE_URL}/game/nhl/game_weeks', text=get_response_stub())

    yfs, _ = make_api_call(is_valid=False)

    yfs.auth_service.refresh_tokens.assert_called_with()


def test_response_code_not_200(requests_mock, mocker):
    requests_mock.get(f'{BASE_URL}/game/nhl/game_weeks', text='Error!', status_code=400)
    with raises(SystemExit) as sys_exit_e:
        make_api_call()
    assert sys_exit_e.type == SystemExit


def test_response_with_metadata(requests_mock):
    requests_mock.get(f'{BASE_URL}/game/nhl/game_weeks', text=get_response_stub())

    _, resp = make_api_call(with_metadata=True)
    assert resp[0] == {'data': 'data'}
    assert resp[1] == 'data2'


def make_api_call(is_valid=True, with_metadata=False):
    yfs = YahooFantasyApi(123456)
    yfs.expires_by = time.time() + 1000 if is_valid else time.time() - 1000
    return yfs, yfs.get_game_weeks(with_metadata)
