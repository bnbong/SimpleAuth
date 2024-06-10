# original : test/conftest.py
# import asyncio
# import pytest
# import pytest_asyncio
#
# from sqlalchemy import event
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
#
# from sqlmodel import SQLModel
#
# from src.core.settings import AppSettings
#
#
# app_settings = AppSettings(_env_file=".env.test")
#
#
# async_engine = create_async_engine(
#     str(app_settings.DATABASE_URI), pool_size=5, echo=True, max_overflow=10
# )
#
# TestingAsyncSessionLocal = sessionmaker(
#     async_engine,
#     expire_on_commit=False,
#     autoflush=False,
#     autocommit=False,
#     class_=AsyncSession,
# )
#
#
# @pytest_asyncio.fixture(scope="function")
# async def session():
#     connection = await async_engine.connect()
#     trans = await connection.begin()
#     async_session = TestingAsyncSessionLocal(bind=connection)
#     nested = await connection.begin_nested()
#
#     @event.listens_for(async_session.sync_session, "after_transaction_end")
#     def end_savepoint(session, transaction):
#         nonlocal nested
#
#         if not nested.is_active:
#             nested = connection.sync_connection.begin_nested()
#
#     yield async_session
#
#     await trans.rollback()
#     await async_session.close()
#     await connection.close()
