from dataclasses import dataclass


@dataclass
class VideoFrameSize:
    """
    Dimensions for how a video clip should be re-sized
    """
    length: int
    width: int
