import os
import shutil
from typing import Dict, Optional

import youtube_dl

from powerhour.args import ArgumentParser
from powerhour.filesystem import VIDEO_DOWNLOAD_DIR_NAME, mkdir_if_not_exists
from powerhour.hooks import DownloadRecorderHook
from powerhour.logging import YouTubeLogger
from powerhour.processing import ClipProcessor
from powerhour.youtube import YouTubeApiClient


def _map_filenames_to_notes_if_possible(
        download_hook: DownloadRecorderHook,
        playlist_url: str,
        youtube_api_key: Optional[str],
) -> Dict[str, Optional[str]]:
    """
    :param download_hook: A download hook with its downloaded filenames already populated
    :param playlist_url: Full URL for a YouTube playlist
    :param youtube_api_key: Optional YouTube API Key, map will be empty if not provided
    :return: Mapping of {downloaded filename : `note` text from corresponding PlaylistItem contentDetails, if exists}
    """
    if youtube_api_key is None:
        return {}

    youtube_api = YouTubeApiClient(youtube_api_key)
    video_ids_to_note_map = youtube_api.map_video_ids_to_note(playlist_url)

    filename_to_note_map = {}
    for filename in download_hook.files_sorted:
        video_id = download_hook.parse_out_video_id(filename)
        filename_to_note_map[filename] = video_ids_to_note_map.get(video_id)

    return filename_to_note_map


def _main():
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()

    download_recorder_hook = DownloadRecorderHook()

    ydl_opts = {
        'format': 'best',
        'logger': YouTubeLogger(),
        'progress_hooks': [download_recorder_hook],
        'outtmpl': os.path.join(VIDEO_DOWNLOAD_DIR_NAME, DownloadRecorderHook.YOUTUBE_DL_OUTPUT_FORMAT),
    }

    shutil.rmtree(VIDEO_DOWNLOAD_DIR_NAME, ignore_errors=True)
    mkdir_if_not_exists(VIDEO_DOWNLOAD_DIR_NAME)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.playlist_url])

    filename_to_note_map = _map_filenames_to_notes_if_possible(
        download_hook=download_recorder_hook,
        playlist_url=arg_parser.extract_playlist_id_from_url(args.playlist_url),
        youtube_api_key=args.youtube_api_key,
    )
    power_hour = ClipProcessor.combine(
        (ClipProcessor(fname, video_notes=filename_to_note_map.get(fname)) for fname in download_recorder_hook.files_sorted),
        clip_length_seconds=60,
    )
    power_hour.write_videofile(os.path.join(VIDEO_DOWNLOAD_DIR_NAME, 'power_hour.mp4'))


if __name__ == '__main__':
    _main()
