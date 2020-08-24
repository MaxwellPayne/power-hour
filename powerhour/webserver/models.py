import argparse
from decimal import Decimal
from typing import Optional

import pydantic

from powerhour.generation.args import ArgumentParser


class GeneratePowerHourRequest(pydantic.BaseModel):
    playlist_url: str
    youtube_api_key: Optional[str]

    @pydantic.validator('playlist_url')
    def validate_playlist_url(cls, v) -> str:
        try:
            ArgumentParser.parse_playlist_url(v)
        except argparse.ArgumentTypeError as e:
            raise ValueError(str(e))

        return v


class GeneratePowerHourJob(pydantic.BaseModel):
    id: str
    playlist_url: str
    completion_percentage: Decimal = Decimal(0)
    videos_processed: int = 0

    class Config:
        orm_mode = True
