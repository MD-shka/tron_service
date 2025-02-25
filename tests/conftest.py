import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.dependencies.db import get_db
from app.main import app
from app.models.base import Base
from app.schemas.pydantic_schemas import WalletInfo

async_engine = create_async_engine("sqlite+aiosqlite:///test.db")
AsyncTestSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
async def async_db_session():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = AsyncTestSessionLocal()
    try:
        yield session
    finally:
        await session.close()
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
def client(async_db_session):
    def override_get_db():
        try:
            yield async_db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
def dummy_get_account_info():
    def _dummy_get_account_info(self, address: str) -> WalletInfo:
        return WalletInfo(address=address, balance=12345678, bandwidth=800, energy=400)

    return _dummy_get_account_info
