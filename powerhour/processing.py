import datetime
from typing import Iterable, Optional

from moviepy.editor import (
    AudioClip,
    AudioFileClip,
    CompositeAudioClip,
    VideoFileClip,
    concatenate_videoclips,
)

from powerhour.filesystem import asset_path


class ClipProcessor:
    def __init__(self, filename: str, video_notes: Optional[str] = None):
        """
        :param filename: Absolute path to a youtube-dl downloaded file
        :param video_notes: Optional `notes` metadata from the video as specified in its YouTube playlist item
        """
        self.filename = filename
        self.video_notes = video_notes
        self.clip = VideoFileClip(filename)

    @property
    def offset_seconds_from_video_notes(self) -> Optional[int]:
        """
        :return: If notes specified a well-formatted clip offset from the beginning, return the number of seconds offset
        """
        if self.video_notes is not None:
            offset_timedelta = self.parse_minutes_seconds(self.video_notes)
            if offset_timedelta is not None:
                return int(offset_timedelta.total_seconds())

        return None

    def extract_subclip(self, clip_length_seconds: int) -> VideoFileClip:
        offset_seconds = self.offset_seconds_from_video_notes
        t_start = offset_seconds if offset_seconds else 0
        return self.clip.subclip(t_start=t_start, t_end=t_start + clip_length_seconds)

    @classmethod
    def combine(cls, processors: Iterable['ClipProcessor'], clip_length_seconds: int) -> VideoFileClip:
        clips = []

        for idx, processor in enumerate(processors):
            clip = processor.extract_subclip(clip_length_seconds)
            if idx > 0:
                # apply transition noise for all clips but the first
                clip = clip.afx(lambda c: CompositeAudioClip([c, cls.ding_crack_audio()]))

            clips.append(clip)

        return concatenate_videoclips(clips)

    @staticmethod
    def ding_crack_audio() -> AudioClip:
        """
        :return: The "ding, crack" audio transition sound clip from static assets
        """
        return AudioFileClip(asset_path('ding_crack.wav'))

    @staticmethod
    def parse_minutes_seconds(value: str) -> Optional[datetime.timedelta]:
        """
        Parse out a minutes:seconds string into timedelta, e.g. "03:01" -> `datetime.timedelta(seconds=181)`
        :return: Timedelta of minutes and seconds, if value could be parsed
        """
        try:
            parsed_datetime = datetime.datetime.strptime(value, '%M:%S')
        except ValueError:
            return None

        return datetime.timedelta(minutes=parsed_datetime.minute, seconds=parsed_datetime.second)
