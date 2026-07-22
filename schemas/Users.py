from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    role: str
    delivery_address: Optional[str]
    station: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    delivery_address: Optional[str] = None
    station: Optional[str] = None

class User(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True
