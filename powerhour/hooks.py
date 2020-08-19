import os
from typing import List


class DownloadRecorderHook:

    # format string youtube-dl must use in order for its output files to be readable by this class
    YOUTUBE_DL_OUTPUT_FORMAT = '%(playlist_index)s___%(id)s___%(title)s.%(ext)s'

    def __init__(self):
        self._downloaded_files: List[str] = []

    def __call__(self, download_hook_payload: dict):
        if download_hook_payload['status'] == 'finished':
            filename = download_hook_payload['filename']
            self._downloaded_files.append(filename)

    @property
    def files_sorted(self) -> List[str]:
        return sorted(self._downloaded_files, key=self.filename_sort_key)

    @staticmethod
    def file_name(absolute_file_path: str) -> str:
        return os.path.split(absolute_file_path)[-1]

    @classmethod
    def filename_sort_key(cls, absolute_file_path: str) -> int:
        playlist_index: str = cls.parse_out_playlist_index(absolute_file_path)
        if playlist_index == 'NA':
            # this video was not part of any playlist, youtube-dl used the value "NA" to signify
            return 0
        return int(playlist_index)

    @classmethod
    def parse_out_playlist_index(cls, absolute_file_path: str) -> str:
        file_name = cls.file_name(absolute_file_path)
        return file_name.split('___')[0]

    @classmethod
    def parse_out_video_id(cls, absolute_file_path: str) -> str:
        file_name = cls.file_name(absolute_file_path)
        return file_name.split('___')[1]
