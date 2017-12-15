from typing import NamedTuple


class LocationCoords(NamedTuple):
    """The latitude and longitude coordinates of a location."""
    lat: float
    long: float


class Weather(NamedTuple):
    """Summary of the weather for a location."""
    low_temperature: float
    high_temperature: float
    description: str
    time: str

    def as_dict(self) -> dict:
        """Return fields as a dict for keyword unpacking."""
        return {
            key: getattr(self, key)
            for key in self._fields
        }
