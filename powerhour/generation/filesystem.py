import errno
import os


MODULE_DIR_NAME = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR_NAME = os.path.join(MODULE_DIR_NAME, 'assets')
VIDEO_DOWNLOAD_DIR_NAME = os.path.join(MODULE_DIR_NAME, 'video_downloads')


def mkdir_if_not_exists(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def asset_path(filename: str) -> str:
    return os.path.join(ASSETS_DIR_NAME, filename)
