from pydantic import BaseModel


class SendGroupMessage(BaseModel):
    message: str
    channel_uuid: str


class SendUserMessage(BaseModel):
    message: str
    name: str
    hash: str
