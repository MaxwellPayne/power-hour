import asyncio
from decimal import Decimal

import proglog

from powerhour.generation.downloader import Downloader
from powerhour.webserver.db import database, generate_power_hour_jobs


class ProgressPercentageLogger(proglog.ProgressBarLogger):

    def __init__(self, job_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_id = job_id
        self.total: int = None
        self.current: int = None
        self._previously_saved_percent: Decimal = Decimal(0)

    @property
    def percent(self) -> Decimal:
        return Decimal((self.current / self.total) * 100).quantize(Decimal('0.0'))

    def bars_callback(self, bar, attr, value, old_value=None):
        if self.bar_is_video_writer(bar):
            if attr == 'total':
                self.total = value
                self.current = 0
                self._previously_saved_percent = Decimal(0)
            elif attr == 'index':
                self.current = value

            percent = self.percent
            if percent - self._previously_saved_percent >= Decimal('0.5'):
                asyncio.get_event_loop().run_until_complete(self.report_completion_percentage(self.job_id, percent))
                self._previously_saved_percent = percent
        elif self.bar_is_youtube_downloader(bar):
            if attr == 'count':
                asyncio.get_event_loop().run_until_complete(self.report_videos_processed(self.job_id, value))
            elif attr == 'missing_video_ids':
                # TODO: handle missing videos
                pass

    def callback(self, **kw):
        message = kw.get('message')
        if message:
            print(message)

    @staticmethod
    def bar_is_video_writer(bar: str) -> bool:
        """
        Determine whether PyMovie is writing a video file
        """
        return bar == 't'

    @staticmethod
    def bar_is_youtube_downloader(bar: str) -> bool:
        """
        Determine whether custom YouTube Downloader class is calling the callback
        """
        return bar == Downloader.PROGRESS_BAR_NAME

    @staticmethod
    async def report_completion_percentage(job_id: str, progress_percent: Decimal):
        query = generate_power_hour_jobs.update(
            generate_power_hour_jobs.c.id == job_id
        ).values(completion_percentage=progress_percent)
        return await database.execute(query)

    @staticmethod
    async def report_videos_processed(job_id: str, videos_processed: int):
        query = generate_power_hour_jobs.update(
            generate_power_hour_jobs.c.id == job_id
        ).values(videos_processed=videos_processed)
        return await database.execute(query)
