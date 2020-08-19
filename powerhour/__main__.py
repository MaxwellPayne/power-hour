import os
import sys

import youtube_dl

from powerhour.filesystem import VIDEO_DOWNLOAD_DIR_NAME, mkdir_if_not_exists
from powerhour.hooks import DownloadRecorderHook
from powerhour.logging import YouTubeLogger
from powerhour.processing import ClipProcessor


if __name__ == '__main__':
    download_hook = DownloadRecorderHook()

    ydl_opts = {
        'format': 'best',
        'logger': YouTubeLogger(),
        'progress_hooks': [download_hook],
        'outtmpl': os.path.join(VIDEO_DOWNLOAD_DIR_NAME, '%(playlist_index)s_%(title)s.%(ext)s'),
    }

    mkdir_if_not_exists(VIDEO_DOWNLOAD_DIR_NAME)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([sys.argv[1]])

    power_hour = ClipProcessor.combine((ClipProcessor(fname) for fname in download_hook.files_sorted), 60)
    power_hour.write_videofile(os.path.join(VIDEO_DOWNLOAD_DIR_NAME, 'power_hour.mp4'))
