from yfantasy_api.api.terminal import TerminalApi
from yfantasy_api.models import User


class UserApi:
    """User Resouce API: An api used for querying user resources

    This acutally leverages the Users Collection api endpoint, but given
    most users won't know their guid and all user information is private
    Yahoo suggests using this endpoint with the `;use_login=1` filter
    to return the user who is authenticated and making the call.

    Attributes
    ----------
    __yfantasy_api: YahooFantasyApi
        The api class responsible for checking the tokens and sending
        the http request
    __url: str
        The base url for user resources
    path: str
        The path to append to the base url; can contain subresources,
        filters, or nothing depending on the builder methods called
    """

    def __init__(self, yfantasy_api):
        """Initialize a new User Resource API

        Parameters
        ----------
        yfantasy_api: YahooFantasyApi
            The api class responsible for checking tokens and sending
            the http request
        """
        self.__yfantasy_api = yfantasy_api
        self.__url = 'users;use_login=1'
        self.path = ''

    def meta(self):
        """Leaves the path empty to make the call return meta information

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        return TerminalApi(self)

    def games(self):
        """Updates the path to include the `games` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/games'
        return TerminalApi(self)

    def teams(self):
        """Updates the path to include the `teams` sub-resource

        Returns a TerminalApi object that provides a `get()` call to
        invoke the query.
        """
        self.path += '/teams'
        return TerminalApi(self)

    def get(self):
        """Invoke the Yahoo Fantasy API GET call to query the User Resource

        The response json is transformed into a User model
        """
        return User(self.__yfantasy_api.get(f'{self.__url}{self.path}')['users']['0']['user'])
