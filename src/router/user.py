# --------------------------------------------------------------------------
# User router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from uuid import UUID

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import create_user, get_user, update_user, delete_user
from src.db.base import DeleteResponse
from src.db.database import get_db
from src.db.models.user import UserResponse, UserCreate, UserUpdate

router = APIRouter(
    prefix="/user",
)


@router.post(
    "/",
    summary="Create a new user.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user_route(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_user(db=db, user=data)


@router.get(
    "/{id}",
    summary="Get a user.",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_route(id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_user(db=db, id=id)


@router.patch(
    "/{id}",
    summary="Update a user.",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def update_user_route(
    id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await update_user(db=db, id=id, user=data)


@router.delete(
    "/{id}",
    summary="Delete a user.",
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponse,
)
async def delete_user_route(id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await delete_user(db=db, id=id)
    return DeleteResponse(deleted=deleted)
