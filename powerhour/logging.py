import logging
import os


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))
LOGGER = logging.getLogger('powerhour')


class YouTubeLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
