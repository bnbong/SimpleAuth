# --------------------------------------------------------------------------
# User의 CRUD testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest

from uuid_extensions import uuid7

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import (
    create_user,
    get_user,
    get_user_by_email,
    update_user,
    delete_user,
)
from src.db.models.user import UserCreate, UserUpdate
from src.helper.exceptions import InternalException


@pytest.mark.asyncio
class TestUserCRUD:
    async def test_create_user(self, get_test_db: AsyncSession):
        user = UserCreate(email="test@example.com")
        created_user = await create_user(get_test_db, user)
        assert created_user.id is not None
        assert created_user.email == user.email
        assert created_user.created_at is not None
        assert created_user.updated_at is not None

    async def test_get_user(self, get_test_db: AsyncSession):
        user = UserCreate(email="test@example.com")
        created_user = await create_user(get_test_db, user)
        retrieved_user = await get_user(get_test_db, created_user.id)
        assert retrieved_user == created_user

    async def test_get_user_by_email(self, get_test_db: AsyncSession):
        user = UserCreate(email="test@example.com")
        created_user = await create_user(get_test_db, user)
        retrieved_user = await get_user_by_email(get_test_db, user.email)
        assert retrieved_user == created_user

    async def test_update_user(self, get_test_db: AsyncSession):
        created_user = await create_user(
            get_test_db, UserCreate(nickname="alice", email="test@example.com")
        )
        updated_user = await update_user(
            get_test_db, created_user.id, UserUpdate(nickname="bob")
        )
        assert updated_user.id == created_user.id
        assert updated_user.email == "test@example.com"
        assert updated_user.nickname == "bob"

    async def test_delete_user(self, get_test_db: AsyncSession):
        created_user = await create_user(get_test_db, UserCreate(email="test@example.com"))
        deleted_count = await delete_user(get_test_db, created_user.id)
        assert deleted_count == 1
        retrieved_user = await get_user(get_test_db, created_user.id)
        assert retrieved_user is None


@pytest.mark.asyncio
class TestUserCRUDFail:
    async def test_create_duplicate_user(self, get_test_db: AsyncSession):
        user = UserCreate(email="test@example.com")
        await create_user(get_test_db, user)
        try:
            await create_user(get_test_db, user)
        except InternalException as e:
            assert e.error_code.value[1] == "SA-006"
            assert e.message == "이미 존재하는 유저입니다."

    async def test_get_nonexistent_user(self, get_test_db: AsyncSession):
        retrieved_user = await get_user(get_test_db, uuid7())
        assert retrieved_user is None

    async def test_get_nonexistent_user_by_email(self, get_test_db: AsyncSession):
        retrieved_user = await get_user_by_email(get_test_db, "nonexistent@example.com")
        assert retrieved_user is None

    async def test_update_nonexistent_user(self, get_test_db: AsyncSession):
        try:
            await update_user(get_test_db, uuid7(), UserUpdate(first_name="alice"))
        except InternalException as e:
            assert e.error_code.value[1] == "SA-004"
            assert e.message == "해당 유저를 찾을 수 없습니다."

    async def test_delete_nonexistent_user(self, get_test_db: AsyncSession):
        deleted_count = await delete_user(get_test_db, uuid7())
        assert deleted_count == 0
