import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from database.core import session, close_session
from database.models import Base, AccountUser
from settings.config import env
from main import app

test_engine = create_async_engine(env.database_url)
test_session = async_sessionmaker(test_engine, autoflush=False, expire_on_commit=False)
Base.metadata.bind = test_engine
session = test_session


async def conn_db():
    async with test_engine.begin() as sos:
        await sos.run_sync(Base.metadata.drop_all)
        await sos.run_sync(Base.metadata.create_all)
    async with session() as sos:
        async with sos.begin():
            account = AccountUser(wallet_uuid=123, deposit=0)
            sos.add(account)
            await sos.commit()


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    await conn_db()
    yield
    await close_session()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
