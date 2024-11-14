from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/wallets")


@router.get("/{WALLET_UUID}/")
async def get_balance_wallet(WALLET_UUID: int):
    return f"Your balance is {WALLET_UUID}"


@router.get("/{WALLET_UUID}/operation/")
async def post_deposit(WALLET_UUID: int):
    return f"Your deposit was changed {WALLET_UUID}"
