from typing import Optional
from pydantic import BaseModel, HttpUrl


class Podcast(BaseModel):
    podcast_link: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None
    artist: Optional[str] = None
    source: Optional[str] = None
