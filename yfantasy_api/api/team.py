from yfantasy_api.api.terminal import TerminalApi
from yfantasy_api.models import Team


class TeamApi:
    """Team Resource API: An api used for querying team resources

    Attributes
    ----------
    __yfantasy_api: YahooFantasyApi
        The api class responsible for checking the tokens and sending
        the http request
    __team_key: str
        The team key built using the game_code and league_id from the
        __yfantasy_api object along with the provided team_id. The
        format is <game-code>.l.<league-id>.t.<team-id>
    __url: str
        The base url for team resources
    path: str
        The path to append to the base url; can contain subresources,
        filters, or nothing depending on the builder methods called
    """
    def __init__(self, yfantasy_api, team_id):
        """Initialize a new Team Resource API

        Parameters
        ----------
        yfantasy_api: YahooFantasyApi
            The api class responsible for checking tokens and sending
            the http request
        """
        self.__yfantasy_api = yfantasy_api
        self.__team_key = f'{self.__yfantasy_api.game_id}.l.{self.__yfantasy_api.league_id}.t.{team_id}'
        self.__url = f'/team/{self.__team_key}'
        self.path = ''

    def meta(self):
        """Leaves the path empty to make the call return meta information

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        return TerminalApi(self)

    def matchups(self, week=None):
        """Updates the path to include the `matchups` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.

        Parameters
        ----------
        week: int
            If a value is provided this will add a `week=<value>`
            filter to the path that filters the results by week.
            If nothing is provided the server will default to the
            current week.
        """
        self.path += '/mathchups'

        if week:
            self.path += f';week={week}'

        return TerminalApi(self)

    def roster(self, date=None, week=None):
        """Updates the path to include the `roster` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.

        Parameters
        ----------
        date: int
            The value to indicate what date the roster data should be
            scoped. If a value is provided this will add a `date=<value>`
            filter.
        week: int
            The value to indicate what week the roster data should be
            scoped. If a value is provided this will add a `week=<value>`
            filter. The server uses the first date in the week when
            returning the filtered roster.
        """
        coverage_filter = self.__build_coverage_filter(week, date)
        self.path += f'/roster{coverage_filter}'
        return PlayerCollectionApi(self)

    def standings(self):
        """Updates the path to include the `standings` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/standings'
        return TerminalApi(self)

    def stats(self):
        """Updates the path to include the `stats` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/stats'
        return TerminalApi(self)

    def get(self):
        """Invoke the Yahoo Fantasy API GET call to query the Team Resource

        The response json is transformed into a Team model
        """
        return Team(self.__yfantasy_api.get(f'{self.__url}{self.path}')['team'])

    def __build_coverage_filter(self, week, date):
        if week and date:
            raise Exception('Only one of \'date\' or \'week\' should be provided.')
        elif week:
            return f';week={week}'
        elif date:
            return f';date={date}'
        else:
            return ''


class PlayerCollectionApi:
    """Players Collection API: Supports querying players sub-resources

    Attributes
    ----------
    __parent_api
        The parent api class that created this object, this parent
        api is used when invoking the query or creating the terminal
        api object.
    """
    def __init__(self, parent_api):
        """Initialize a new Players Collection API object

        Parameters
        ----------
        parent_api
            The parent api class that created this object, this parent
            api is used when invoking the query or creating the terminal
            api object.
        """
        self.__parent_api = parent_api

    def stats(self, date=None, season=None, week=None):
        """Updates the path to include the 'stats' sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.

        This method supports changing the requested scope for player
        stats, but only one of `date`, `season`, or `week` can be
        provided.

        Parameters
        ----------
        date: str
            The value to indicate the date of the player stats to return.
            If a value is provided this will add a `;type=date;date=<value>`
            filter. The date must be provided in a 'YYYY-MM-DD' format.
        season: int
            The value to indicate the season of the players stats to return.
            If a value is provided this will add a `;type=season;season=<value>`
            filter.
        week:int
            The value to indicate the week of the players stats to return.
            If a value is provided this will add a `;type=week;week=<value>`
            filter.
        """
        coverage_filter = self.__build_coverage_filter(date, season, week)
        self.__parent_api.path += f'/players/stats{coverage_filter}'
        return TerminalApi(self.__parent_api)

    def get(self):
        """Invoke the parent API `get()` call
        """
        return self.__parent_api.get()

    def __build_coverage_filter(self, date, season, week):
        if bool(date) + bool(season) + bool(week) > 1:
            raise Exception('Only one of \'date\', \'season\', or \'week\' should be provided.')
        elif date:
            return f';type=date;date={date}'
        elif season:
            return f';type=season;season={season}'
        elif week:
            return f';type=week;week={week}'
        else:
            return ''
