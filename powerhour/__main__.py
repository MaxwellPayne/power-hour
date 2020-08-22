import os
import shutil

from powerhour.generation.args import ArgumentParser
from powerhour.generation.datastructures import VideoFrameSize
from powerhour.generation.downloader import Downloader
from powerhour.generation.filesystem import VIDEO_DOWNLOAD_DIR_NAME, mkdir_if_not_exists
from powerhour.generation.logging import LOGGER, ProgressPercentageLogger, YouTubeLogger
from powerhour.generation.processing import ClipProcessor
from powerhour.generation.youtube import YouTubeApiClient


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
    filename_to_note_map = YouTubeApiClient.map_filenames_to_notes_if_possible(
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
    power_hour.write_videofile(
        os.path.join(VIDEO_DOWNLOAD_DIR_NAME, 'power_hour.mp4'),
        logger=ProgressPercentageLogger() if False else 'bar',
    )
    LOGGER.info('Done!')


if __name__ == '__main__':
    _main()
