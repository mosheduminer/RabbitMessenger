from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

import enum
from uuid import uuid1


class ChannelType(enum.Enum):
    USER = "USER"
    GROUP = "GROUP"


class Channel(Base):
    __tablename__ = "channels"

    id = Column(UUID, primary_key=True, default=lambda: uuid1().hex)
    name = Column(String, nullable=True)
    type = Column(Enum(ChannelType))
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
