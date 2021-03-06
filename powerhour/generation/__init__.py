import os
import shutil
from typing import Optional

import proglog

from powerhour.generation.args import ArgumentParser
from powerhour.generation.datastructures import VideoFrameSize
from powerhour.generation.downloader import Downloader
from powerhour.generation.filesystem import VIDEO_DOWNLOAD_DIR_NAME, mkdir_if_not_exists
from powerhour.generation.logging import LOGGER, YouTubeLogger
from powerhour.generation.processing import ClipProcessor
from powerhour.generation.youtube import YouTubeApiClient


def generate_powerhour(
        playlist_url: str,
        youtube_api_key: Optional[str],
        progress_logger: Optional[proglog.ProgressBarLogger] = None,
        download_directory_path: str = VIDEO_DOWNLOAD_DIR_NAME
):
    # TODO: tmp directories
    ydl_opts = {
        'logger': YouTubeLogger(),
        'outtmpl': os.path.join(download_directory_path, Downloader.YOUTUBE_DL_OUTPUT_FORMAT),
        'ignoreerrors': True,
    }

    shutil.rmtree(download_directory_path, ignore_errors=True)
    mkdir_if_not_exists(download_directory_path)
    LOGGER.info(f'Download starting for playlist: {playlist_url}')
    with Downloader(ydl_opts, progress_logger=progress_logger) as ydl:
        ydl.download([playlist_url])

    missing_video_ids = ydl.find_missing_video_ids()
    if missing_video_ids:
        missing_video_names = [ydl.video_ids_and_titles[video_id] for video_id in missing_video_ids]
        LOGGER.error('The following videos failed to download:' + '\n        - '.join([''] + missing_video_names))

    LOGGER.info('Finished YouTube downloads, combining video clips')
    filename_to_note_map = YouTubeApiClient.map_filenames_to_notes_if_possible(
        downloader=ydl,
        playlist_url=ArgumentParser.extract_playlist_id_from_url(playlist_url),
        youtube_api_key=youtube_api_key,
    )
    power_hour = ClipProcessor.combine(
        (ClipProcessor(fname, video_notes=filename_to_note_map.get(fname)) for fname in ydl.files_sorted),
        clip_length_seconds=60,
        uniform_frame_size=VideoFrameSize(length=720, width=1280),
    )
    LOGGER.info('Writing power hour video to file')
    output_file_path = os.path.join(download_directory_path, 'power_hour.mp4')
    power_hour.write_videofile(
        output_file_path,
        logger=progress_logger if progress_logger is not None else 'bar',
    )
    if progress_logger is not None:
        progress_logger.bars_callback(GENERATE_POWERHOUR_PROGRESS_BAR_NAME, 'output_video', output_file_path)

    LOGGER.info('Done!')


GENERATE_POWERHOUR_PROGRESS_BAR_NAME = 'generate_powerhour'
