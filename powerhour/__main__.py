import os
import shutil
from typing import Dict, Optional

from powerhour.args import ArgumentParser
from powerhour.datastructures import VideoFrameSize
from powerhour.downloader import Downloader
from powerhour.filesystem import VIDEO_DOWNLOAD_DIR_NAME, mkdir_if_not_exists
from powerhour.logging import YouTubeLogger, LOGGER
from powerhour.processing import ClipProcessor
from powerhour.youtube import YouTubeApiClient


def _map_filenames_to_notes_if_possible(
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

    youtube_api = YouTubeApiClient(youtube_api_key)
    video_ids_to_note_map = youtube_api.map_video_ids_to_note(playlist_url)

    filename_to_note_map = {}
    for filename in downloader.files_sorted:
        video_id = downloader.parse_out_video_id(filename)
        filename_to_note_map[filename] = video_ids_to_note_map.get(video_id)

    return filename_to_note_map


def _main():
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()

    ydl_opts = {
        'logger': YouTubeLogger(),
        'outtmpl': os.path.join(VIDEO_DOWNLOAD_DIR_NAME, Downloader.YOUTUBE_DL_OUTPUT_FORMAT),
        'ignoreerrors': True,
    }

    shutil.rmtree(VIDEO_DOWNLOAD_DIR_NAME, ignore_errors=True)
    mkdir_if_not_exists(VIDEO_DOWNLOAD_DIR_NAME)
    LOGGER.info(f'Download starting for playlist: {args.playlist_url}')
    with Downloader(ydl_opts) as ydl:
        ydl.download([args.playlist_url])

    missing_video_ids = ydl.find_missing_video_ids()
    if missing_video_ids:
        missing_video_names = [ydl.video_ids_and_titles[video_id] for video_id in missing_video_ids]
        LOGGER.error('The following videos failed to download:' + '\n        - '.join([''] + missing_video_names))

    LOGGER.info('Finished YouTube downloads, combining video clips')
    filename_to_note_map = _map_filenames_to_notes_if_possible(
        downloader=ydl,
        playlist_url=arg_parser.extract_playlist_id_from_url(args.playlist_url),
        youtube_api_key=args.youtube_api_key,
    )
    power_hour = ClipProcessor.combine(
        (ClipProcessor(fname, video_notes=filename_to_note_map.get(fname)) for fname in ydl.files_sorted),
        clip_length_seconds=60,
        uniform_frame_size=VideoFrameSize(length=720, width=1280),
    )
    LOGGER.info('Writing power hour video to file')
    power_hour.write_videofile(os.path.join(VIDEO_DOWNLOAD_DIR_NAME, 'power_hour.mp4'))
    LOGGER.info('Done!')


if __name__ == '__main__':
    _main()
