# --------------------------------------------------------------------------
# User의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
# import pytest
# import pytest_asyncio
#
# from test.routes.conftest import BaseTestRouter
#
#
# @pytest.mark.asyncio
# class TestUserAPI(BaseTestRouter):
#     @pytest_asyncio.fixture(autouse=True)
#     async def setup(self, client):
#         pass
#
#     async def test_create_user(self, client):
#         # given
#         data = {"email": "test@example.com", "password": "password"}
#
#         # when
#         response = await client.post("/users/", json=data)
#
#         # then
#         assert response.status_code == 201
#         assert response.json()["email"] == data["email"]
