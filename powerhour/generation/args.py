import argparse
import urllib.parse


class ArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super().__init__(
            description='Make a power hour from a YouTube playlist',
        )
        self.add_argument('--youtube-api-key', dest='youtube_api_key', type=str, default=None)
        self.add_argument('playlist_url', type=self.parse_playlist_url)

    @classmethod
    def parse_playlist_url(cls, value: str) -> str:
        """
        Validate that the provided value is a properly formatted YouTube playlist URL, if so return it
        """
        try:
            cls.extract_playlist_id_from_url(value)
            return value
        except Exception:
            raise argparse.ArgumentTypeError(f'"{value}" is not a valid YouTube playlist url')

    @staticmethod
    def extract_playlist_id_from_url(value: str) -> str:
        """
        :param value: YouTube playlist URL (e.g. "https://www.youtube.com/playlist?list=ABCD")
        :return: The playlist identifier specified in the url query params (e.g. "ABCD")
        """
        playlist_arg_query_params = urllib.parse.parse_qs(urllib.parse.urlparse(value).query)
        return playlist_arg_query_params['list'][0]
