import logging
import os
from decimal import Decimal

import proglog


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))
LOGGER = logging.getLogger('powerhour')


class YouTubeLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class ProgressPercentageLogger(proglog.ProgressBarLogger):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total: int = None
        self.current: int = None
        self._previously_displayed_percent: Decimal = Decimal(0)

    @property
    def percent(self) -> Decimal:
        return Decimal((self.current / self.total) * 100).quantize(Decimal('0.0'))

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == 'total':
            self.total = value
            self.current = 0
            self._previously_displayed_percent = Decimal(0)
        elif attr == 'index':
            self.current = value

        percent = self.percent
        if percent - self._previously_displayed_percent >= Decimal('0.5'):
            print(f'Progress {percent}%')
            self._previously_displayed_percent = percent

    def callback(self, **kw):
        message = kw.get('message')
        if message:
            print(message)
