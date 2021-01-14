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
    def __init__(self):
        self.__set_credentials()
        self.__set_tokens()
        self.__cache_tokens()

    ###################
    # Private methods
    ###################
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

    ##################
    # Public methods
    ##################
    def refresh_tokens(self):
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
        return self.__access_token

    def get_refresh_token(self):
        return self.__refresh_token

    def get_expires_by(self):
        return self.__expires_by
