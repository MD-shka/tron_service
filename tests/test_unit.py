import pytest
from sqlalchemy import text

from app.schemas.pydantic_schemas import WalletRequestInput
from app.services.api_service import get_wallet_info


@pytest.mark.asyncio
async def test_database_record_unit(async_db_session, monkeypatch, dummy_get_account_info):
    monkeypatch.setattr("app.services.tron_service.TronService.get_account_info", dummy_get_account_info)
    result = await async_db_session.execute(text("SELECT COUNT(*) FROM wallet_requests;"))
    count_before = result.scalar() or 0

    dummy_request = WalletRequestInput(address="TYav58BSjcRnUmvJkDLX365kGms2q9q6wZ")
    await get_wallet_info(async_db_session, dummy_request)

    result = await async_db_session.execute(text("SELECT COUNT(*) FROM wallet_requests;"))
    count_after = result.scalar() or 0

    assert count_after == count_before + 1
