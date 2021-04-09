from yfantasy_api.api.terminal import TerminalApi
from yfantasy_api.models import League


class LeagueApi:
    """League Resource API: An api used for querying league resources

    Attributes
    ----------
    __yfantasy_api: YahooFantasyApi
        The api class responsible for checking the tokens and sending
        the http request
    __league_key: str
        The league key built using the game_code and league_id from the
        __yfantasy_api object; the format is <game-code>.l.<league-id>
    __url: str
        The base url for league resources
    path: str
        The path to append to the base url; can contain subresources,
        filters, or nothing depending on the builder methods called
    """

    def __init__(self, yfantasy_api):
        """Initialize a new League Resource API

        Parameters
        ----------
        yfantasy_api: YahooFantasyApi
            The api class responsible for checking tokens and sending
            the http request
        """
        self.__yfantasy_api = yfantasy_api
        self.__league_key = f'{self.__yfantasy_api.game_id}.l.{self.__yfantasy_api.league_id}'
        self.__url = f'/league/{self.__league_key}'
        self.path = ''

    def draft_results(self):
        """Updates the path to include the `draftresults` sub-resource

        Returns a DraftResultsCollectionApi object that provides methods
        for adding further sub-resources or invoking the query
        """
        self.path += '/draftresults'
        return DraftResultsCollectionApi(self)

    def meta(self):
        """Leaves the path empty to make the call return meta information

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        return TerminalApi(self)

    def players(self, start=0, count=25, status=None, search=None):
        """Updates the path to include the `players` sub-resource

        Returns a PlayersCollectionApi object that provides methods
        for adding further sub-resources or invoking the query

        Parameters
        ----------
        start: int
            The value to indicate what offset to start the players
            list at. For example: `start=0` begins at the first
            player while `start=1` begins at the second. (default: 0)
        count: int
            The value to indicate how many players to return in the
            list. If the value exceeds the max value the server will
            ignore it and use the max value. (max: 25, default: 25)
        status: str
            The player status used to filter the list. If a value
            is provided, this will add a `;status=<value>` filter to
            the path. The accepted values are 'A' (all), 'FA' (free
            agent), 'W' (waivers), 'T' (taken)
        search: str
            A string to used to filter the list by player names. If
            a value is provided, this will add a `;search=<value>`
            filter to the path. The server accepts any string and
            performs substring matching for all player names. If a
            match isn't found the list of players will be empy.
        """
        self.path += f'/players;start={start};count={count}'

        if search:
            self.path += f';search={search}'

        if status:
            self.path += f';status={status}'

        return PlayersCollectionApi(self)

    def scoreboard(self, week=None):
        """Updates the path to include the `scoreboard` sub-resource

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
        self.path += '/scoreboard'

        if week:
            self.path += f';week={week}'

        return TerminalApi(self)

    def settings(self):
        """Updates the path to include the `settings` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/settings'
        return TerminalApi(self)

    def standings(self):
        """Updates the path to include the `standings` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/standings'
        return TerminalApi(self)

    def teams(self):
        """Updates the path to include the `teams` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/teams'
        return TerminalApi(self)

    def transactions(self, ttype=None, team_id=None, count=None, start=None):
        """Updates the path to include the `transactions` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.

        Parameters
        ----------
        ttype: str
            The value to indicate what type of transactions to return
            in the list. If a value is provided, this will add a
            `;type=<value` filter to the path. The accepted values are
            'add' (returns add, drop, and add/drop), 'drop' (returns
            add, drop, and add/drop), 'commish', and 'trade'. The values
            'waiver' and 'pending_trade' are also accepted, but require
            the `team_id` parameter to be provided as well.
        team_id: int
            The id of the team to use when filtering the list. If a value
            is provided, this will add a `;team_key=<gm>.l.<lg>.<value>`.
            For simplicity the id is converted into a key for the filter.
        count: int
            The value to indicate how many transactions to return in the
            list. Unlike the players collection, there doesn't seem to be
            a maximum value for transactions. (default: 25)
        start: int
            The value to indicate what offset to start the transactions
            list at. For example: `start=0` begins at the most recent
            transaction while `start=1` begins at the second most recent.
            (default: 0)
        """
        self.path += '/transactions'

        if ttype in ['waiver', 'pending_trade'] and not team_id:
            raise Exception(f'\'team_id\' must be provided when using \'{ttype}\'.')

        if ttype:
            self.path += f';type={ttype}'
        if team_id:
            self.path += f';team_key={self.__league_key}.t.{team_id}'
        if count:
            self.path += f';count={count}'
        if start:
            self.path += f';start={start}'

        return TerminalApi(self)

    def get(self):
        """Invoke the Yahoo Fantasy API GET call to query the League Resource

        The response json is transformed into a League model
        """
        return League(self.__yfantasy_api.get(f'{self.__url}{self.path}')['league'])


class DraftResultsCollectionApi:
    """Draft Results API: Supports querying draft results sub-resources

    Attributes
    ----------
    __parent_api
        The parent api class that created this object, this parent
        api is used when invoking the query or creating the terminal
        api object.
    """

    def __init__(self, parent_api):
        """Initialize a new Draft Results API object

        Parameters
        ----------
        parent_api
            The parent api class that created this object, this parent
            api is used when invoking the query or creating the terminal
            api object.
        """
        self.__parent_api = parent_api

    def players(self):
        """Updates the path to include the 'players' sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.__parent_api.path += '/players'
        return TerminalApi(self.__parent_api)

    def get(self):
        """Invoke the parent API `get()` call
        """
        return self.__parent_api.get()


class PlayersCollectionApi:
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

    def draft_analysis(self):
        """Updates the path to include the 'draft_analysis' sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.__parent_api.path += '/draft_analysis'
        return TerminalApi(self.__parent_api)

    def ownership(self):
        """Updates the path to include the 'ownership' sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.__parent_api.path += '/ownership'
        return TerminalApi(self.__parent_api)

    def percent_owned(self):
        """Updates the path to include the 'percent_owned' sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.__parent_api.path += '/percent_owned'
        return TerminalApi(self.__parent_api)

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
        self.__parent_api.path += f'/stats{coverage_filter}'
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
