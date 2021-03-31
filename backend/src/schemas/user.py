from typing import Type
from pydantic import BaseModel, EmailStr
from . import Channel, Membership


class UserBase(BaseModel):
    """
    Base class - you shouldn't be using this outside of this module
    """

    email: EmailStr


class UserAuth(UserBase):
    password: str


class UserCreate(UserAuth):
    name: str


class UserInternal(UserCreate):
    id: int
    hash: str
    owned_channels: list[Channel]

    class Config:
        orm_mode = True


class UserInternalWithChannels(UserInternal):
    memberships: list[Membership]

    class Config:
        orm_mode = True


class UserExternal(BaseModel):
    name: str
    hash: str

    class Config:
        orm_mode = True
