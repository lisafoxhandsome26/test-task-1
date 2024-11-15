import pytest


@pytest.mark.parametrize(
        "uuid, result", [(123, "Your balance"), (12, "Your wallet das not exists")]
    )
async def test_get_balance(ac, uuid, result):
    """Тест для получения профиля пользователя"""
    response = await ac.get(f"/api/v1/wallets/{uuid}/")
    assert response.status_code == 200
    assert result in response.text


data_for_test = [
    (123, {"operationType": "DEPOSI", "amount": 1000}, "No known operation Type"),
    (123, {"operationType": "DEPOSIT", "amounts": 1000}, "The parameters do not exist"),

    (123, {"operationType": 1555, "amount": 1000}, "OperationType mast be STRING"),
    (123, {"operationType": "DEPOSIT", "amount": -50}, "positive number"),
    (123, {"operationType": "DEPOSIT", "amount": "dsda"}, "Amount mast be INTEGER"),
]


@pytest.mark.parametrize(
        "uuid, json_data, result", data_for_test
    )
async def test_post_deposit(ac, uuid, json_data, result):
    """Тест для получения профиля пользователя"""
    response = await ac.post(f"/api/v1/wallets/{uuid}/operation/", json=json_data)
    assert result in response.text
