from yfantasy_api.api.terminal import TerminalApi
from yfantasy_api.models import Game


class GamesApi:
    """Game Collection API: An api used for querying game collections

    Attributes
    ----------
    __yfantasy_api: YahooFantasyApi
        The api class responsible for checking the tokens and sending
        the http request
    __url: str
        The base url for game collections
    path: str
        The path to append to the base url; can contain subresources,
        filters, or nothing depending on the builder methods called
    """

    def __init__(self, yfantasy_api):
        """Initialize a new Game Resource API

        Parameters
        ----------
        yfantasy_api: YahooFantasyApi
            The api class responsible for checking tokens and sending
            the http request
        """
        self.__yfantasy_api = yfantasy_api
        self.__url = 'games'
        self.path = ''

    def get(self, is_available=None, game_codes=[], seasons=[]):
        """Invoke the Yahoo Fantasy API GET call to query the Game Collections

        The response json is transformed into a a list of Game models

        Parameters
        ----------
            is_available: bool
                A flag that tells the server to only include active
                games or inactive games; if no value is passed the
                `is_available` filter is not included in the request
            game_codes: list
                A list of game codes (ex. 'nfl', 'nhl', 403, 386, etc)
                used to filter the list of games
            seasons: list
                A list of seasons (ex. 2021, 2020, etc) used to filter
                the list of games
        """
        if is_available is not None:
            self.path += f';is_available={int(is_available)}'
        if game_codes:
            game_codes = ','.join(game_codes)
            self.path += f';game_codes={game_codes}'
        if seasons:
            seasons = ','.join(map(str, seasons))
            self.path += f';seasons={seasons}'

        games = self.__yfantasy_api.get(f'{self.__url}{self.path}')['games']
        return [Game(games[str(d)]['game']) for d in range(games['count'])]


class GameApi:
    """Game Resource API: An api used for querying game resources

    Attributes
    ----------
    __yfantasy_api: YahooFantasyApi
        The api class responsible for checking the tokens and sending
        the http request
    __url: str
        The base url for game resources
    path: str
        The path to append to the base url; can contain subresources,
        filters, or nothing depending on the builder methods called
    """

    def __init__(self, yfantasy_api):
        """Initialize a new Game Resource API

        Parameters
        ----------
        yfantasy_api: YahooFantasyApi
            The api class responsible for checking tokens and sending
            the http request
        """
        self.__yfantasy_api = yfantasy_api
        self.__url = f'game/{self.__yfantasy_api.game_id}'
        self.path = ''

    def game_weeks(self):
        """Updates the path to include the `game_weeks` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/game_weeks'
        return TerminalApi(self)

    def position_types(self):
        """Updates the path to include the `position_types` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/position_types'
        return TerminalApi(self)

    def roster_positions(self):
        """Updates the path to include the `roster_positions` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/roster_positions'
        return TerminalApi(self)

    def stat_categories(self):
        """Updates the path to include the `stat_categories` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/stat_categories'
        return TerminalApi(self)

    def get(self):
        """Invoke the Yahoo Fantasy API GET call to query the Game Resource

        The response json is transformed into a Game model
        """
        return Game(self.__yfantasy_api.get(f'{self.__url}{self.path}')['game'])
