from uuid import UUID
from src.models.channel import ChannelType
from pydantic import BaseModel
from typing import Optional


class Channel(BaseModel):
    id: UUID
    name: Optional[str]
    type: ChannelType
    owner_id: int

    class Config:
        orm_mode = True
