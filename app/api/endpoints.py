from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.pydantic_schemas import WalletInfo, WalletRecord, WalletRequestInput
from app.services.api_service import get_history_service, get_wallet_info

router = APIRouter(
    responses={
        200: {"description": "Successfully"},
        400: {"description": "Bad request, invalid input or data not found"},
        422: {"description": "Validation error, invalid input format"},
        500: {"description": "Internal server error"},
    }
)


@router.post("/wallet_info", response_model=WalletInfo)
async def wallet_info_endpoint(request: WalletRequestInput, db: AsyncSession = Depends(get_db)):
    try:
        wallet_info = await get_wallet_info(db, request)
        return wallet_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", response_model=list[WalletRecord])
async def get_history(page: int = Query(1, ge=1), size: int = Query(10, ge=1), db: AsyncSession = Depends(get_db)):
    try:
        history = await get_history_service(db, page, size)
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
