from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    channel_id = Column(UUID, ForeignKey("channels.id"), index=True)

    users = relationship("User", back_populates="memberships")
    channel = relationship("Channel")
