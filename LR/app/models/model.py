from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    description: Optional[str]

class UserCreate(UserBase):

    class Config:
        extra = "forbid"

    pass

class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[str]
    description: Optional[str]

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
        extra = "forbid"
        validate_assignment = True