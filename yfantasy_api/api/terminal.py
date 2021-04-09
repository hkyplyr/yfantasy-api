class TerminalApi:
    """A terminal class that provides a method to invoke the query

    This helps with the fluent API and ensures that invoking the
    query only occurs with a `get()` call.

    For example: api.league().players().stats().get() is only
    invoked using the `get()` call.

    Attributes
    ----------
    __parent_api
        The parent api class that created this object, this parent
        api is used when invoking the query.
    """

    def __init__(self, parent_api):
        """Initialize a new Terminal API object

        Parameters
        ----------
        parent_api
            The parent api class that created this object, this parent
            api is used when invoking the query.
        """
        self.__parent_api = parent_api

    def get(self):
        """Invoke the parent API `get()` call
        """
        return self.__parent_api.get()
