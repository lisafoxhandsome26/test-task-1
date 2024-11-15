from sqlalchemy import Column, Integer, DECIMAL
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):
    pass


class AccountUser(Base):
    __tablename__ = "AccountUser"

    id = Column(Integer(), primary_key=True, index=True)
    deposit = Column(DECIMAL())
    wallet_uuid = Column(Integer(), index=True)

    def __repr__(self):
        return f"Deposit for wallet_uuid - {self.wallet_uuid} - {self.deposit}"
