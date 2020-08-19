from typing import Iterable

from moviepy.editor import VideoFileClip, concatenate_videoclips


class ClipProcessor:
    def __init__(self, filename: str):
        self.filename = filename
        self.clip = VideoFileClip(filename)

    def extract_subclip(self, clip_length_seconds: int) -> VideoFileClip:
        return self.clip.subclip(t_start=0, t_end=clip_length_seconds)

    @staticmethod
    def combine(processors: Iterable['ClipProcessor'], clip_length_seconds: int) -> VideoFileClip:
        return concatenate_videoclips(
            [processor.extract_subclip(clip_length_seconds) for processor in processors]
        )
