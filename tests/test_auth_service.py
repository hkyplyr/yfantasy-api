import json
import time
import requests_mock

from pytest import fixture
from unittest import mock

from yfantasy_api import auth


@fixture(autouse=True)
def setup(tmpdir):
    auth.TOKEN_FILE = str(tmpdir.mkdir('load_tokens').join('.tokens.json'))


def test_load_tokens(tmpdir):
    with open('tests/resources/existing_tokens.json') as et, \
         open(auth.TOKEN_FILE, 'w+') as tokens_file:
        existing_tokens_contents = json.loads(et.read())
        tokens_file.write(json.dumps(existing_tokens_contents))
        tokens_file.flush()

        auth_service = auth.AuthenticationService()
        assert auth_service.get_access_token() == 'ex_access_token'
        assert auth_service.get_refresh_token() == 'ex_refresh_token'
        assert auth_service.get_expires_by() == 'ex_expires_by'


def test_refresh_tokens(requests_mock, tmpdir):
    requests_mock.post(f'{auth.AUTHORIZE_URL}', text='d')
    __builtins__['input'] = lambda _: 'code'

    auth.TOKEN_FILE = str(tmpdir.mkdir('refresh_tokens').join('.tokens.json'))
    with open('tests/resources/refreshed_tokens.json') as rt, \
         open('tests/resources/initial_tokens.json') as it:
        requests_mock.post(auth.TOKEN_URL, text=it.read())

        auth_service = auth.AuthenticationService()
        assert auth_service.get_access_token() == 'access_token'
        assert auth_service.get_refresh_token() == 'refresh_token'
        initial_expires_by = auth_service.get_expires_by()
        assert initial_expires_by > time.time()

        requests_mock.post(auth.TOKEN_URL, text=rt.read())
        auth_service.refresh_tokens()
        assert auth_service.get_access_token() == 'ref_access_token'
        assert auth_service.get_refresh_token() == 'ref_refresh_token'
        assert auth_service.get_expires_by() > initial_expires_by
