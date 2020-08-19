import os
from typing import List


class DownloadRecorderHook:
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
    def filename_sort_key(absolute_file_path: str) -> int:
        file_name = os.path.split(absolute_file_path)[-1]
        file_index_prefix = file_name.split('_')[0]
        if file_index_prefix == 'NA':
            return 0
        return int(file_index_prefix)
