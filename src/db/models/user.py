# --------------------------------------------------------------------------
# User model의 ORM 및 스키마를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from sqlmodel import SQLModel, Field

from pydantic import EmailStr

from src.db.base import IdMixin, TimestampMixin


class UserBase(SQLModel):
    nickname: str = None
    email: EmailStr = Field(
        nullable=False, index=True, sa_column_kwargs={"unique": True}
    )
    is_active: bool = True


class User(IdMixin, TimestampMixin, UserBase, table=True):
    __tablename__ = "users"


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    nickname: str = None
    email: EmailStr = None
    is_active: bool = None


class UserResponse(User, table=False):
    ...
