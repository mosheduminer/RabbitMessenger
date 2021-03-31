from pydantic import BaseModel


class Membership(BaseModel):
    id: int
    user_id: int
    channel_id: int
