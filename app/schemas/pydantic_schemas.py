from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from tronpy.keys import to_base58check_address


class WalletRequestInput(BaseModel):
    address: str

    @field_validator("address")
    def validate_address(cls, value):
        try:
            return to_base58check_address(value)
        except ValueError:
            raise ValueError("Invalid address")


class WalletInfo(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: int


class WalletRecord(WalletRequestInput):
    id: int
    requested_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
