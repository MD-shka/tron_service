import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dependencies.db import get_db
from app.main import app
from app.models.base import Base
from app.schemas.pydantic_schemas import WalletInfo

engine = create_engine("sqlite:///test.db")
TestSessionLocal = sessionmaker(bind=engine, autocommit=False)


@pytest.fixture(scope="session")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def dummy_get_account_info():
    def _dummy_get_account_info(self, address: str) -> WalletInfo:
        return WalletInfo(address=address, balance=12345678, bandwidth=800, energy=400)

    return _dummy_get_account_info
