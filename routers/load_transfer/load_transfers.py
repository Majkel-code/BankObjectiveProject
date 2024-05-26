from fastapi import APIRouter, Body

from users.credits.credit_maker import CreditMaker
from users.transfers.transfer_maker import TransferMaker
from users.transfers.transfer_reader import TransferReader

router = APIRouter(
    prefix="/transfers",
)


@router.post("/last_history")
async def receive_data(data: dict = Body(...)):
    return TransferReader().check_history(data.get("acc_id"))


@router.post("/newtransfer")
async def new_transfer(data: dict = Body(...)):
    print(data)
    print("RECEIVE FROM WEB DATA ^^^^")
    if data["to_acc"] == "9999 9999 9999 9999":
        return CreditMaker().setup_credit_calculation(
            excess_amount=data["amount"], operation="EXCESS", **data
        )
    return TransferMaker().save_transfer(**data)


@router.get("/defoult")
async def get_defoult():
    return TransferReader().take_def_transactions()
