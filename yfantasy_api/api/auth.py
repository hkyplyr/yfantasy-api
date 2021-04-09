import json
import os
import requests
import time

ACCESS_TOKEN = 'access_token'
EXPIRES_BY = 'expires_by'
EXPIRES_IN = 'expires_in'
REFRESH_TOKEN = 'refresh_token'
TOKEN_FILE = '.tokens.json'

AUTHORIZE_URL = 'https://api.login.yahoo.com/oauth2/request_auth'
TOKEN_URL = 'https://api.login.yahoo.com/oauth2/get_token'
BASE_URL = 'https://fantasysports.yahooapis.com/fantasy/v2'


class AuthenticationService:
    """Responsible for obtaining, checking, and refreshing tokens as needed

    This service has two main ways to authenticate a user with Yahoo.
    If the user hasn't used this library before the service obtains a new set
    of oauth tokens from Yahoo via the `__client_id` and `__client_secret`.
    If the user has used this library before and a `.tokens.json` file exists
    the `__access_token` is read in from that file and checked for expiry. If
    the token has already expired this service will refresh the token, otherwise
    it is good to be used.

    Attribute
    ----------
    __client_id: str
        The user's client_id read in through the `CLIENT_ID` env variable
    ___client_secret: str
        The user's client_secret read in through the `CLIENT_SECRET` env variable
    __access_token: str
        The current access token used for authenticating requests to Yahoo
    __refresh_token: str
        The current refresh token used for refreshing the access token
    __expires_by: float
        The expiry of the current access token, used to determine when to refresh
    """

    def __init__(self):
        """Initialize a new AuthenticationService

        The initialization consists of reading in the client id and secret
        from their respective env variables, loading existing tokens or
        retrieving new tokens, and finally caching the tokens into the
        `.tokens.json` file.
        """
        self.__set_credentials()
        self.__set_tokens()
        self.__cache_tokens()

    def refresh_tokens(self):
        """Retrieve a new access token using the refresh token.

        When this method is called a new request is built to obtain
        a new set of oauth tokens from Yahoo by providing the
        `__client_id`, `__client_secret`, and `__refresh_token`.
        """
        data = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'redirect_uri': 'oob',
            'refresh_token': self.__refresh_token,
            'grant_type': 'refresh_token',
        }

        tokens = requests.post(TOKEN_URL, data=data).json()
        self.__cache_refreshed_tokens(tokens)

    def get_access_token(self):
        """A simple getter for obtaining the access token.
        """
        return self.__access_token

    def get_refresh_token(self):
        """A simple getter for obtaining the refresh token.
        """
        return self.__refresh_token

    def get_expires_by(self):
        """A simple getter for obtaining the access token expiry.
        """
        return self.__expires_by

    def __set_credentials(self):
        self.__client_id = os.getenv('CLIENT_ID')
        self.__client_secret = os.getenv('CLIENT_SECRET')

    def __set_tokens(self):
        if os.path.exists(TOKEN_FILE):
            self.__load_tokens()
        else:
            self.__get_tokens()

    def __load_tokens(self):
        with open(TOKEN_FILE, 'r') as f:
            loaded_tokens = json.loads(f.read())
        self.__access_token = loaded_tokens[ACCESS_TOKEN]
        self.__refresh_token = loaded_tokens[REFRESH_TOKEN]
        self.__expires_by = loaded_tokens[EXPIRES_BY]

    def __get_tokens(self):
        code = self.__get_auth_code()
        requested_tokens = self.__request_tokens(code)

        self.__access_token = requested_tokens[ACCESS_TOKEN]
        self.__refresh_token = requested_tokens[REFRESH_TOKEN]
        self.__expires_by = requested_tokens[EXPIRES_IN] + time.time()

    def __get_auth_code(self):
        params = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'redirect_uri': 'oob',
            'response_type': 'code',
            'language': 'en-us',
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(AUTHORIZE_URL, params=params, headers=headers)
        print(response.url)

        return input('Enter code: ')

    def __request_tokens(self, code):
        data = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'redirect_uri': 'oob',
            'code': code,
            'grant_type': 'authorization_code',
        }

        return requests.post(TOKEN_URL, data=data).json()

    def __cache_tokens(self):
        tokens = {
            ACCESS_TOKEN: self.__access_token,
            REFRESH_TOKEN: self.__refresh_token,
            EXPIRES_BY: self.__expires_by
        }

        with open(TOKEN_FILE, 'w+') as f:
            f.write(json.dumps(tokens))

    def __cache_refreshed_tokens(self, tokens):
        self.__access_token = tokens[ACCESS_TOKEN]
        self.__refresh_token = tokens[REFRESH_TOKEN]
        self.__expires_by = tokens[EXPIRES_IN] + time.time()

        self.__cache_tokens()
