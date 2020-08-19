from typing import Any, Dict, Optional

import requests


class YouTubeApiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_playlist_items(self, playlist_id: str) -> Dict[str, Any]:
        """
        Make an API call to list `Playlistitems` for the provided playlist ID
        See: https://developers.google.com/youtube/v3/docs/playlistItems/list
        :return: JSON dictionary of the API response
        :raise: Exception if HTTP status code was not a success
        """
        res = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params={
            'part': 'contentDetails',
            'playlistId': playlist_id,
            'key': self.api_key,
        })
        res.raise_for_status()
        return res.json()

    def map_video_ids_to_note(self, playlist_id: str) -> Dict[str, Optional[str]]:
        """
        Call the playlist items API endpoint for the given playlist ID, then look at the response and
        map all playlist video IDs to the value of their `note` field in `contentDetails`, or to
        `None` if the video ID has no `note`.
        :return: Mapping of {YouTube video ID : `note` text from corresponding PlaylistItem contentDetails, if exists}
        """
        playlist_json = self.fetch_playlist_items(playlist_id)

        mapping = {}
        for playlist_item in playlist_json['items']:
            content_details = playlist_item['contentDetails']
            mapping[content_details['videoId']] = content_details.get('note')

        return mapping
