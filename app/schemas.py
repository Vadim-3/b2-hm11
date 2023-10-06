from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    birthday_date: date
    phone_numbers: str = Field(min_length=10, max_length=13)
    emails: EmailStr
    other_description: Optional[str]


class UserResponse(UserSchema):
    id: int
    emails: EmailStr

    class Config:
        orm_mode = True
