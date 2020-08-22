from typing import Any, Dict, Optional

import requests

from powerhour.generation.downloader import Downloader


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
        You can write this `note` value to playlist items by visiting:
            https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID&advanced_settings=1&disable_polymer=1
            Then hovering over the "More" menu for a song and clicking "Add / edit notes"
        :return: Mapping of {YouTube video ID : `note` text from corresponding PlaylistItem contentDetails, if exists}
        """
        playlist_json = self.fetch_playlist_items(playlist_id)

        mapping = {}
        for playlist_item in playlist_json['items']:
            content_details = playlist_item['contentDetails']
            mapping[content_details['videoId']] = content_details.get('note')

        return mapping

    @classmethod
    def map_filenames_to_notes_if_possible(
            cls,
            downloader: Downloader,
            playlist_url: str,
            youtube_api_key: Optional[str],
    ) -> Dict[str, Optional[str]]:
        """
        :param downloader: A downloader with its downloaded filenames already populated
        :param playlist_url: Full URL for a YouTube playlist
        :param youtube_api_key: Optional YouTube API Key, map will be empty if not provided
        :return: Mapping of {downloaded filename : `note` text from corresponding PlaylistItem contentDetails, if exists}
        """
        if not youtube_api_key:
            return {}

        youtube_api = cls(youtube_api_key)
        video_ids_to_note_map = youtube_api.map_video_ids_to_note(playlist_url)

        filename_to_note_map = {}
        for filename in downloader.files_sorted:
            video_id = downloader.parse_out_video_id(filename)
            filename_to_note_map[filename] = video_ids_to_note_map.get(video_id)

        return filename_to_note_map
