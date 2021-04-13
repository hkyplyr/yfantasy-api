import requests_mock
import time

from pytest import fixture, raises
from pytest_mock import mocker

from yfantasy_api.api.api import YahooFantasyApi
from yfantasy_api.api.auth import AuthenticationService


@fixture(autouse=True)
def setup(mocker):
    mocker.patch.object(AuthenticationService, '_AuthenticationService__cache_tokens').return_val = None
    mocker.patch.object(AuthenticationService, '_AuthenticationService__set_tokens').return_val = None
    mocker.patch.object(AuthenticationService, 'get_access_token').return_val = 'access_token'
    mocker.patch.object(AuthenticationService, 'get_expires_by').return_val = 'expires_by'
    mocker.patch.object(AuthenticationService, 'get_refresh_token').return_val = 'refresh_token'
    mocker.patch.object(AuthenticationService, 'refresh_tokens').return_val = None


def get_response_stub():
    with open('tests/resources/game/game.json') as f:
        return f.read()


def test_get_resource_valid_tokens(requests_mock):
    requests_mock.get(f'{YahooFantasyApi.base_url}/game/nhl', text=get_response_stub())
    yfs, _ = make_api_call(is_valid=True)
    yfs.auth_service.refresh_tokens.assert_not_called()


def test_get_resource_invalid_tokens(requests_mock):
    requests_mock.get(f'{YahooFantasyApi.base_url}/game/nhl', text=get_response_stub())
    yfs, _ = make_api_call(is_valid=False)
    yfs.auth_service.refresh_tokens.assert_called_with()


def test_response_code_not_200(requests_mock, mocker):
    requests_mock.get(f'{YahooFantasyApi.base_url}/game/nhl', text='Error!', status_code=400)
    with raises(SystemExit) as sys_exit_e:
        make_api_call()
    assert sys_exit_e.type == SystemExit


def make_api_call(is_valid=True, with_metadata=False):
    yfs = YahooFantasyApi(123456, 'nhl', timeout=0)
    yfs.expires_by = time.time() + 1000 if is_valid else time.time() - 1000
    return yfs, yfs.game().get()
