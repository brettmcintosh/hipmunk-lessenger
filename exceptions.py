class Error(Exception):
    """Base class that can provide context for template rendering."""
    def __init__(self, message, data=None):
        self.message = message
        self.data = data

    def __str__(self):
        return self.message

    def get_context(self) -> dict:
        """Return the data as a dict."""
        return {'data': self.data}


class ParseError(Error):
    """Error for a query that can't be parsed."""
    pass


class LocationError(Error):
    """Error for a location that can't be resolved."""
    pass


class WeatherError(Error):
    """Error for a location with no weather results."""
    pass
