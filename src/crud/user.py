# --------------------------------------------------------------------------
# User Model CRUD 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, delete

from src.db.models.user import UserCreate, User, UserUpdate
from src.helper.exceptions import InternalException, ErrorCode


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(**user.dict())
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise InternalException(
            error_code=ErrorCode.CONFLICT,
            message="이미 존재하는 유저입니다.",
        )


async def get_user(db: AsyncSession, id: UUID) -> User:
    query = select(User).where(User.id == id)
    response = await db.execute(query)
    return response.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email)
    response = await db.execute(query)
    return response.scalar_one_or_none()


async def update_user(db: AsyncSession, id: UUID, user: UserUpdate) -> User:
    db_user = await get_user(db, id)
    if not db_user:
        raise InternalException(
            error_code=ErrorCode.NOT_FOUND, message="해당 유저를 찾을 수 없습니다."
        )

    for k, v in user.dict(exclude_unset=True).items():
        setattr(db_user, k, v)

    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise InternalException(
            error_code=ErrorCode.CONFLICT,
            message="다른 유저 정보와 중복되는 정보가 있습니다.",
        )


async def delete_user(db: AsyncSession, id: UUID) -> int:
    query = delete(User).where(User.id == id)
    response = await db.execute(query)
    await db.commit()
    return response.rowcount
