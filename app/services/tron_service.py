import os

from dotenv import load_dotenv
from tronpy import Tron
from tronpy.providers import HTTPProvider

from app.schemas.pydantic_schemas import WalletInfo

load_dotenv()

API_KEY = os.getenv("API_KEY")


class TronService:
    def __init__(self):
        self.client = Tron(HTTPProvider("https://api.trongrid.io", api_key=API_KEY))

    def get_account_info(self, wallet_address: str) -> WalletInfo:
        try:
            account = self.client.get_account(wallet_address)
            bandwidth = account.get("net_window_size", 0) - account.get("net_usage", 0)
            account_resource = account.get("account_resource", {})
            energy = account_resource.get("energy_window_size", 0) - account_resource.get("energy_usage", 0)
            balance = account.get("balance", 0)
            return WalletInfo(address=wallet_address, balance=balance, bandwidth=bandwidth, energy=energy)
        except Exception as e:
            raise Exception(f"Failed to get wallet info from Tron network. Reason: {e}")
