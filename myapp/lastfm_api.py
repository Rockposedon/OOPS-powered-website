# import requests
# import json
# import logging
# from django.conf import settings

# class LastFMAPI:
#     BASE_URL = "http://ws.audioscrobbler.com/2.0/"

#     def __init__(self, api_key, shared_secret):
#         # self.api_key = api_key
#         # self.shared_secret = shared_secret
#         # self.logger = logging.getLogger(__name__)
#         self.api_key = settings.LASTFM_API_KEY
#         self.shared_secret = settings.LASTFM_SHARED_SECRET

#     def search_tracks(self, query):
#         params = {
#             'method': 'track.search',
#             'track': query,
#             'api_key': self.api_key,
#             'format': 'json',
#         }

#         try:
#             response = requests.get(self.BASE_URL, params=params)
#             response.raise_for_status()  # Raise an HTTPError for bad responses

#             try:
#                 result = response.json().get('results', {}).get('trackmatches', {}).get('track', [])
#                 return result
#             except json.JSONDecodeError as json_error:
#                 self.logger.error(f"Error decoding JSON: {json_error}")
#                 return []
#         except requests.exceptions.RequestException as request_error:
#             # Handle request errors (e.g., network issues)
#             self.logger.error(f"Error making Last.fm API request: {request_error}")
#             return []
#         except Exception as unexpected_error:
#             # Handle other exceptions
#             self.logger.error(f"Unexpected error: {unexpected_error}")
#             return []

import requests
import json
import logging
from django.conf import settings

class LastFMAPI:
    BASE_URL = "http://ws.audioscrobbler.com/2.0/"

    def __init__(self, api_key, shared_secret):
        self.api_key = settings.LASTFM_API_KEY
        self.shared_secret = settings.LASTFM_SHARED_SECRET
        self.logger = logging.getLogger(__name__)

    def search_tracks(self, query):
        params = {
            'method': 'track.search',
            'track': query,
            'api_key': self.api_key,
            'format': 'json',
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            try:
                # Extract relevant information from the API response and create Track instances
                tracks = []
                for result in response.json().get('results', {}).get('trackmatches', {}).get('track', []):
                    track = Track(
                        name=result.get('name', ''),
                        artist=result.get('artist', ''),
                        preview_url=result.get('url', '')  # Adjust this accordingly based on your API response
                    )
                    tracks.append(track)

                return tracks
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Error decoding JSON: {json_error}")
                return []
        except requests.exceptions.RequestException as request_error:
            # Handle request errors (e.g., network issues)
            self.logger.error(f"Error making Last.fm API request: {request_error}")
            return []
        except Exception as unexpected_error:
            # Handle other exceptions
            self.logger.error(f"Unexpected error: {unexpected_error}")
            return []

class Track:
    def __init__(self, name, artist, preview_url):
        self.name = name
        self.artist = artist
        self.preview_url = preview_url
