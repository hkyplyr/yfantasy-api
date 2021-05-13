import json
import time
import requests_mock

from pytest import fixture
from unittest import mock

from yfantasy_api.api import auth


@fixture(autouse=True)
def setup(tmpdir):
    auth.TOKEN_FILE = str(tmpdir.mkdir('load_tokens').join('.tokens.json'))


def test_load_tokens(tmpdir):
    existing_tokens = {
        "access_token": "ex_access_token",
        "refresh_token": "ex_refresh_token",
        "expires_by": "ex_expires_by"
    }
    with open(auth.TOKEN_FILE, 'w') as token_file:
        json.dump(existing_tokens, token_file)

    auth_service = auth.AuthenticationService()
    assert auth_service.get_access_token() == 'ex_access_token'
    assert auth_service.get_refresh_token() == 'ex_refresh_token'
    assert auth_service.get_expires_by() == 'ex_expires_by'


def test_refresh_tokens(requests_mock, tmpdir):
    initial_tokens = {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
        "expires_in": 3600
    }

    refreshed_tokens = {
        "access_token": "ref_access_token",
        "refresh_token": "ref_refresh_token",
        "expires_in": 3600
    }

    requests_mock.post(f'{auth.AUTHORIZE_URL}', text='d')
    __builtins__['input'] = lambda _: 'code'

    auth.TOKEN_FILE = str(tmpdir.mkdir('refresh_tokens').join('.tokens.json'))
    requests_mock.post(auth.TOKEN_URL, text=json.dumps(initial_tokens))

    auth_service = auth.AuthenticationService()
    assert auth_service.get_access_token() == 'access_token'
    assert auth_service.get_refresh_token() == 'refresh_token'
    initial_expires_by = auth_service.get_expires_by()
    assert initial_expires_by > time.time()

    requests_mock.post(auth.TOKEN_URL, text=json.dumps(refreshed_tokens))
    auth_service.refresh_tokens()
    assert auth_service.get_access_token() == 'ref_access_token'
    assert auth_service.get_refresh_token() == 'ref_refresh_token'
    assert auth_service.get_expires_by() > initial_expires_by
