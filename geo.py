import googlemaps

import secrets


# Create a singleton gmaps client
geo_service = googlemaps.Client(key=secrets.GMAPS_API_KEY)
