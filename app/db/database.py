from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models.base import Base

DATABASE_URL = "sqlite+aiosqlite:///./tron.db"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
