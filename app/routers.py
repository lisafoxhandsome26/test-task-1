from fastapi import APIRouter, Body, Request
from fastapi.templating import Jinja2Templates
from database import queries
from .validators import validation_json
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/api/v1/wallets")
templates = Jinja2Templates(directory="templates")


@router.get("/{WALLET_UUID}/", response_class=HTMLResponse)
async def get_balance_wallet(request: Request, WALLET_UUID: int):
    deposit = await queries.get_wallet_by_uuid(WALLET_UUID)
    context = {"request": request}

    if deposit:
        context["wallet"] = WALLET_UUID
        context["deposit"] = deposit.deposit
        return templates.TemplateResponse("get_wallet.html", context)

    return templates.TemplateResponse("get_wallet.html", context=context)


@router.post("/{WALLET_UUID}/operation/")
async def post_deposit(request: Request, WALLET_UUID: int, data=Body()):
    operationType = data.get("operationType", None)
    amount = data.get("amount", None)
    context = {"request": request}

    result = validation_json(operationType, amount)
    if result:
        context["error"] = f"Error {result['Error']}"
        return templates.TemplateResponse("post_deposit.html", context)

    deposit = await queries.get_wallet_by_uuid(WALLET_UUID)
    if deposit:
        if deposit.deposit < amount and operationType == "WITHDRAW":
            context["error"] = "Error Your deposit is Null or we try to withdraw more then required"
            return templates.TemplateResponse("post_deposit.html", context)

        if operationType == "DEPOSIT":
            await queries.increase_deposit(WALLET_UUID, amount)
            context["message"] = f"Deposit was increase to {amount}"

        elif operationType == "WITHDRAW":
            await queries.reduce_deposit(WALLET_UUID, amount)
            context["message"] = f"Deposit was reduce to {amount}"
        else:
            context["message"] = "No known operation Type"
    else:
        context["message"] = "Your wallet das not exists"

    return templates.TemplateResponse("post_deposit.html", context)


