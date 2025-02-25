from sqlalchemy.future import select

from app.models.model import WalletRequest
from app.schemas.pydantic_schemas import WalletRequestInput


async def create_wallet_request(db, wallet_address: WalletRequestInput) -> None:
    wallet_record = WalletRequest(address=wallet_address.address)
    db.add(wallet_record)
    await db.commit()


async def get_wallet_requests(db, skip: int, limit: int) -> list[WalletRequest]:
    result = await db.execute(
        select(WalletRequest).order_by(WalletRequest.requested_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()
