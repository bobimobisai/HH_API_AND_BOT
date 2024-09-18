from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Union
from datetime import date
import uuid


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str
    tg_user_id: Optional[int] = Field(None, description="ID пользователя в Telegram")

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "tg_user_id": 123456789,
            }
        }


class NoteCreate(BaseModel):
    user_id: uuid.UUID
    title: str
    text: str
    tags: Optional[List[str]] = []


class NoteUpdate(BaseModel):
    title: Optional[str]
    text: Optional[str]
    tags: Optional[List[str]] = []


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str
