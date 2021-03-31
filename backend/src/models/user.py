from sqlalchemy import Column, Integer, String, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from random import choice
from string import digits

from .base import Base


def generate_hash(length=5):
    return "".join([choice(digits) for _ in range(length)])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    hash = Column(String, nullable=False, default=generate_hash)

    name_hash_constraint = UniqueConstraint(name, hash)
    name_hash_index = Index("name", "hash")
    # email_password_index = Index("email", "password")

    owned_channels = relationship("Channel")
    memberships = relationship("Membership", back_populates="users")
