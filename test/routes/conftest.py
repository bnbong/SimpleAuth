# --------------------------------------------------------------------------
# pytest의 router test configuration을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient

from src import create_app
from src.db.database import get_db
from test.conftest import app_settings


class BaseTestRouter:
    @pytest_asyncio.fixture(scope="function")
    async def client(self, session):
        app = create_app(app_settings)
        app.dependency_overrides[get_db] = lambda: session
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c
