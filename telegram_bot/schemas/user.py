from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: str


class User(UserBase):
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
