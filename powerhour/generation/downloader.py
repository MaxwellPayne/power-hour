import os
from typing import Dict, List, Optional

import proglog
import youtube_dl

from powerhour.generation.filesystem import VIDEO_DOWNLOAD_DIR_NAME
from powerhour.generation.logging import LOGGER


class Downloader(youtube_dl.YoutubeDL):

    # format string youtube-dl must use in order for its output files to be readable by this class
    YOUTUBE_DL_OUTPUT_FORMAT = '%(playlist_index)s___%(id)s___%(title)s.%(ext)s'

    # Name this class uses when reporting to the progress bar
    PROGRESS_BAR_NAME = 'yt'

    def __init__(self, params=None, auto_init=True, progress_logger: Optional[proglog.ProgressBarLogger]=None):
        super().__init__(params=params, auto_init=auto_init)
        self.video_ids_and_titles: Dict[str, str] = {}
        self._video_file_paths: List[str] = []
        self._progress_logger = progress_logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        if exc_type is None:
            self._video_file_paths = self._find_downloaded_video_file_paths()

    def process_info(self, info_dict):
        ret = super().process_info(info_dict)
        # capture the video ID once it's done downloading
        video_id, title = info_dict['id'], info_dict['title']
        self.video_ids_and_titles[video_id] = title
        LOGGER.info(f'Finished processing {video_id}: {title}')
        if self._progress_logger is not None:
            self._progress_logger.bars_callback(
                self.PROGRESS_BAR_NAME,
                'count',
                len(self.video_ids_and_titles),
                old_value=len(self.video_ids_and_titles) - 1,
            )

        return ret

    @property
    def files_sorted(self) -> List[str]:
        return sorted(self._video_file_paths, key=self.filename_sort_key)

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

    def find_missing_video_ids(self):
        absolute_file_paths_in_video_dir = self._absolute_file_paths_in_video_dir()
        missing_video_ids = set(self.video_ids_and_titles.keys())

        for video_id in tuple(missing_video_ids):
            for fname in absolute_file_paths_in_video_dir:
                if f'___{video_id}___' in fname:
                    missing_video_ids.remove(video_id)
                    break

        missing_video_ids = list(missing_video_ids)
        if self._progress_logger is not None:
            self._progress_logger.bars_callback(self.PROGRESS_BAR_NAME, 'missing_video_ids', missing_video_ids)

        return missing_video_ids

    def _find_downloaded_video_file_paths(self):
        absolute_file_paths_in_video_dir = self._absolute_file_paths_in_video_dir()

        video_file_paths = []
        for video_id in self.video_ids_and_titles.keys():
            for fname in absolute_file_paths_in_video_dir:
                if f'___{video_id}___' in fname:
                    video_file_paths.append(fname)
                    break

        return video_file_paths

    @staticmethod
    def _absolute_file_paths_in_video_dir():
        paths = []
        for dirpath, _, filenames in os.walk(VIDEO_DOWNLOAD_DIR_NAME):
            for fname in filenames:
                paths.append(os.path.abspath(os.path.join(dirpath, fname)))

        return paths
