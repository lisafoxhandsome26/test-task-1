from fastapi import APIRouter, Body
from database import queries
from .validators import validation_json
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1/wallets")


@router.get("/{WALLET_UUID}/", response_class=JSONResponse)
async def get_balance_wallet(WALLET_UUID: int):
    deposit = await queries.get_wallet_by_uuid(WALLET_UUID)
    if deposit:
        return JSONResponse({"deposit": int(deposit.deposit), "wallet": WALLET_UUID})

    return JSONResponse({"message": "Your wallet das not exists"})


@router.post("/{WALLET_UUID}/operation/")
async def post_deposit(WALLET_UUID: int, data=Body()):
    operationType = data.get("operationType", None)
    amount = data.get("amount", None)

    result = validation_json(operationType, amount)
    if result:
        return JSONResponse({"error": f"Error {result['Error']}"})

    deposit = await queries.get_wallet_by_uuid(WALLET_UUID)
    if deposit:
        if deposit.deposit < amount and operationType == "WITHDRAW":
            return JSONResponse({"error": "Error Your deposit is Null or we try to withdraw more then required"})

        if operationType == "DEPOSIT":
            await queries.increase_deposit(WALLET_UUID, amount)
            message = f"Deposit was increase to {amount}"

        elif operationType == "WITHDRAW":
            await queries.reduce_deposit(WALLET_UUID, amount)
            message = f"Deposit was reduce to {amount}"

        else:
            message = "No known operation Type"
    else:
        message = "Your wallet das not exists"

    return JSONResponse({"message": message})

# Развернуть в docker-compose все
# Подключить миграции
