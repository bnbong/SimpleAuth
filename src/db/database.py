# --------------------------------------------------------------------------
# Database 연결에 사용되는 로직을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings


engine_options = settings.DATABASE_OPTIONS

engine = create_async_engine(str(settings.DATABASE_URI), **engine_options)

SessionLocal = sessionmaker(  # noqa
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Dependency
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
