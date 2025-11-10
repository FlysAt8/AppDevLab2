from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    id: int
    username: str
    email: str
    description: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[str]
    description: Optional[str]

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True