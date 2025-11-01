from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class GeneratePostRequest(BaseModel):
    prompt: str
    is_public: bool = False
    author_name: str = ""  # Valor por defecto string vacío

class PostBase(BaseModel):
    title: str
    content: str
    is_public: bool = False
    author_name: str = ""  # Valor por defecto string vacío

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True