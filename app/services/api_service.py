from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.repository import create_wallet_request, get_wallet_requests
from app.schemas.pydantic_schemas import WalletInfo, WalletRecord, WalletRequestInput
from app.services.tron_service import TronService


async def get_wallet_info(db: AsyncSession, wallet_address: WalletRequestInput) -> WalletInfo:
    account_info = TronService().get_account_info(wallet_address.address)
    await create_wallet_request(db, wallet_address)
    return account_info


async def get_history_service(db: AsyncSession, page: int, size: int) -> list[WalletRecord]:
    skip = (page - 1) * size
    return await get_wallet_requests(db, skip, size)
