import pytest

from database import queries


data_for_test = [
    (123, "Your balance"),
    (12, "Your wallet das not exists")
]


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
        "uuid, result", data_for_test
    )
async def test_get_balance(ac, uuid, result):
    response = await ac.get(f"/api/v1/wallets/{uuid}/")
    assert response.status_code == 200
    assert result in response.text


data_for_test_bad = [
    (123, {"operationType": "DEPOSI", "amount": 1000}, "No known operation Type"),
    (123, {"operationType": "DEPOSIT", "amounts": 1000}, "The parameters do not exist"),

    (123, {"operationType": 1555, "amount": 1000}, "OperationType mast be STRING"),
    (123, {"operationType": "DEPOSIT", "amount": -50}, "positive number"),
    (123, {"operationType": "DEPOSIT", "amount": "dsda"}, "Amount mast be INTEGER"),

    (12, {"operationType": "DEPOSIT", "amount": 500}, "Your wallet das not exists"),
]


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
        "uuid, json_data, result", data_for_test_bad
    )
async def test_post_deposit_bad_json(ac, uuid, json_data, result):
    response = await ac.post(f"/api/v1/wallets/{uuid}/operation/", json=json_data)
    assert result in response.text


data_for_test_good = [
    (123, {"operationType": "DEPOSIT", "amount": 1000}, 1000, "Deposit was increase"),
    (123, {"operationType": "WITHDRAW", "amount": 500}, 500, "Deposit was reduce"),

    (123, {"operationType": "WITHDRAW", "amount": 600}, 500, "we try to withdraw more then required"),
]


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
        "uuid, json_data, result_db, resp", data_for_test_good
    )
async def test_post_deposit_good_json(ac, uuid, json_data, result_db, resp):
    response = await ac.post(f"/api/v1/wallets/{uuid}/operation/", json=json_data)
    deposit = await queries.get_wallet_by_uuid(uuid)
    assert result_db == int(deposit.deposit)
    assert resp in response.text
