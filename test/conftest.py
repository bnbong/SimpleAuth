# --------------------------------------------------------------------------
# pytest의 기본 configuration을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import asyncio
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlmodel import SQLModel

from src.core.settings import AppSettings


app_settings = AppSettings(_env_file=".env.test")


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


test_engine = create_async_engine(
    str(app_settings.DATABASE_URI), **app_settings.DATABASE_OPTIONS
)


@pytest_asyncio.fixture
async def get_test_db():
    test_session_local = AsyncSession(bind=test_engine)  # type: ignore
    try:
        yield test_session_local
    finally:
        await test_session_local.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db():
    print("initialize test database")
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)