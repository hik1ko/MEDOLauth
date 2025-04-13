from enum import Enum

from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    PATIENT = "patient"
    DOCTOR = "doctor"


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: UserRoleEnum = UserRoleEnum.PATIENT

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)

