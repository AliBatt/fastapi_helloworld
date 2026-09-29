from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    phone: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=5, max_length=255)
    phone: Optional[str] = Field(default=None, min_length=5, max_length=20)
    password: Optional[str] = Field(default=None, min_length=6, max_length=72)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: Optional[str]
    created_at: datetime


class CreatePost(BaseModel):
    title: str = Field(min_length=5, max_length=255)
    content: str = Field(min_length=5, max_length=255)
    author_id: int
