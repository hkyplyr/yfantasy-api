import requests
import sys
import time

from yfantasy_api.api.auth import AuthenticationService
from yfantasy_api.api.game import GameApi, GamesApi
from yfantasy_api.api.league import LeagueApi
from yfantasy_api.api.team import TeamApi
from yfantasy_api.api.user import UserApi


class YahooFantasyApi:
    """Yahoo Fantasy API: Used for querying resources and collections from Yahoo fantasy

    This class provides different methods for building and invoking
    queries for various Yahoo Fantasy resources and collections.

    Prior to each call to Yahoo, this class checks the existing tokens to
    ensure they are not yet yet expired, if they are the tokens are quickly
    refreshed without user input, otherwise the call proceeds.

    Attributes
    ----------
    base_url: str
        The base url for all yahoo fantasy sports api calls
    league_id: str
        The user provided league_id
    game_id: str
        The user provided game_id
    auth_service: AuthenticationService
        The authentication service object used for checken tokens are
        still valid and refreshing tokens when needed
    access_token: str
        The token used for authenticating requests to yahoo
    refresh_token: str
        The token used to refresh the access_token once its expired
    expires_by: float
        The timestamp indicating when the current access_token expires
    __timout: int
        The timeout that the client should wait before sending an http
        request. Used to avoid errors caused by too many requests
    """

    base_url = 'https://fantasysports.yahooapis.com/fantasy/v2'

    def __init__(self, league_id, game_id, timeout=1):
        self.league_id = league_id
        self.game_id = game_id
        self.auth_service = AuthenticationService()
        self.__timeout = timeout
        self.__set_tokens()

    def game(self):
        """Build a query for a game resource

        Returns a GameApi object that provides methods for including
        various sub-resources supported by the Game resource
        """
        return GameApi(self)

    def games(self):
        """Build a query for the game collection

        Returns a GamesApi object that supports filtering the game
        collection by various filters.
        """
        return GamesApi(self)

    def league(self):
        """Build a query for a league resource

        Returns a LeagueApi object that provides methods for including
        various sub-resources supported by the League resource
        """
        return LeagueApi(self)

    def team(self, team_id):
        """Build a query for a team resource

        Returns a TeamApi object that provides methods for including
        various sub-resources supported by the Team resource

        Parameters
        ----------
        team_id: str
            The team_id used to scope the resulting query
        """
        return TeamApi(self, team_id)

    def user(self):
        """Build a query for a user resource

        Returns a UserApi object that provides methods for including
        various sub-resources supported by the User resource
        """
        return UserApi(self)

    def get(self, path):
        """Invoke the query built by the api object calling this method

        Parameters
        ----------
        path: str
            The path built by the api object calling this method
        """
        return self.__get_resource(path)

    def __get_resource(self, path):
        self.__check_tokens()
        params = {'format': 'json'}
        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        url = '{}/{}'.format(self.base_url, path)

        time.sleep(self.__timeout)

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()['fantasy_content']
        else:
            print(response.status_code, response.text)
            sys.exit()

    def __set_tokens(self):
        self.access_token = self.auth_service.get_access_token()
        self.refresh_token = self.auth_service.get_refresh_token()
        self.expires_by = self.auth_service.get_expires_by()

    def __check_tokens(self):
        if time.time() > self.expires_by - 300:
            self.auth_service.refresh_tokens()
            self.__set_tokens()
