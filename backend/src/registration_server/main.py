from itertools import count
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Session
from src.schemas.user import UserCreate
from src import models, schemas

app = FastAPI()
# {
#   "email": "user@example.com",
#   "name": "test-user",
#   "hash": "89118"
# }

@app.post("/register", response_model=schemas.UserExternal)
async def register(user_to_create: UserCreate, session: AsyncSession = Depends(Session)):
    for i in count():
        try:
            user = models.User(**user_to_create.dict())
            async with session.begin():
                session.add(user)
                break
        except IntegrityError as e:
            # try 10 times
            if i > 9:
                raise HTTPException(status.HTTP_409_CONFLICT, e)
    async with session.begin():
        session.add(models.Channel(owner_id=user.id, type=models.ChannelType.USER))
    return schemas.UserExternal(**user.__dict__)
