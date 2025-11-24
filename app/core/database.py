from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
# async_sessionmaker is preferred for SQLAlchemy 1.4+ async usage
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Backwards-compatibility alias: some modules import AsyncSessionLocal
AsyncSessionLocal = async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency: yield a session per request and commit at the end.
    Commits if the request succeeds, rollbacks on exception, and always closes the session.
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def init_db():
    from app.shared.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
