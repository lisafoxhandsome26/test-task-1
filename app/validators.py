def validation_json(operationType: str, amount: int) -> dict:
    if operationType is None or amount is None:
        return {"Error": "The parameters do not exist or are not written correctly"}

    if operationType and amount:
        if not isinstance(operationType, str):
            return {"Error": "OperationType mast be STRING"}
        if not isinstance(amount, int) or amount <= 0:
            return {"Error": "Amount mast be INTEGER and positive number"}
