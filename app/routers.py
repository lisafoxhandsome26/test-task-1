from fastapi import APIRouter, Body

from database import queries

router = APIRouter(prefix="/api/v1/wallets")


def validation_json(operationType: str, amount: int) -> dict:
    if operationType is None or amount is None:
        return {"Error": "The parameters do not exist or are not written correctly"}

    if operationType and amount:
        if not isinstance(operationType, str):
            return {"Error": "OperationType mast be STRING"}
        if not isinstance(amount, int):
            return {"Error": "Amount mast be INTEGER"}


@router.get("/{WALLET_UUID}/")
async def get_balance_wallet(WALLET_UUID: int):
    deposit = await queries.get_wallet_by_uuid(WALLET_UUID)

    if deposit:
        return f"<h2>Your balance is {WALLET_UUID} - {deposit.deposit}</h2>"

    return "<h2>Your wallet das not exists</h2>"


@router.post("/{WALLET_UUID}/operation/")
async def post_deposit(WALLET_UUID: int, data=Body()):
    operationType = data.get("operationType", None)
    amount = data.get("amount", None)

    result = validation_json(operationType, amount)
    if result:
        return f"Error {result['error']}"

    if WALLET_UUID == 123:
        if operationType == "DEPOSIT":
            return f"Deposit was posted to {amount}"
        elif operationType == "WITHDRAW":
            return f"Deposit was deleted to {amount}"
        else:
            return "No known operation Type"
    else:
        return "Your wallet das not exists"
