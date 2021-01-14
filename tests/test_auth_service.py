from yfantasy_api.auth import AuthenticationService, AUTHORIZE_URL, TOKEN_URL, TOKEN_FILE
import requests_mock
from unittest import mock
from pytest import fixture
from yfantasy_api import auth

TOKEN_RESPONSE = """
    {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
        "expires_in": 3600
    }
"""


@fixture(autouse=True)
def setup(requests_mock, tmpdir):
    requests_mock.post(f'{AUTHORIZE_URL}', text='d')
    requests_mock.post(f'{TOKEN_URL}', text=TOKEN_RESPONSE)
    tmp_dir = tmpdir.mkdir('sub')
    tmp_dir = tmp_dir.join('.tokens.json')
    auth.TOKEN_FILE = str(tmp_dir)

def test():
    original_input = __builtins__['input']
    __builtins__['input'] = lambda _: 'code'

    auth_service = AuthenticationService()

    __builtins__['input'] = original_input
