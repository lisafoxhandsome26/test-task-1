from sqlalchemy import select, update
from .models import AccountUser
from .core import session


async def get_wallet_by_uuid(uuid: int) -> AccountUser:
    stm = select(AccountUser).filter_by(wallet_uuid=uuid)
    async with session() as sos:
        result = await sos.execute(stm)
        return result.scalars().one_or_none()


async def increase_deposit(uuid: int, amount: int) -> None:
    stm = update(AccountUser).filter_by(wallet_uuid=uuid).values(deposit=AccountUser.deposit + amount)
    async with session() as sos:
        await sos.execute(stm)
        await sos.commit()


async def reduce_deposit(uuid: int, amount: int) -> None:
    stm = update(AccountUser).filter_by(wallet_uuid=uuid).values(deposit=AccountUser.deposit - amount)
    async with session() as sos:
        await sos.execute(stm)
        await sos.commit()
