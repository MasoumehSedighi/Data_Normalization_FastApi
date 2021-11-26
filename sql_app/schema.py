from typing import Optional
from pydantic import BaseModel


class ContactBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth: Optional[str]
    gender: Optional[str]
    is_married: Optional[str]
    phone: Optional[str]


class Contact(ContactBase):
    first_name: Optional[str]

    class Config:
        orm_mode = True

