from fastapi import APIRouter, Body
from users.transfers.transfer_reader import TransferReader
from users.transfers.transfer_maker import TransferMaker


router = APIRouter(
    prefix="/transfers",
)


@router.post("/last_history")
async def receive_data(data: dict = Body(...)):
    return TransferReader().check_history(data.get("acc_id"))



@router.post("/newtransfer")
async def new_transfer(data: dict = Body(...)):
    return TransferMaker().save_transfer(**data)



@router.get("/defoult")
async def new_transfer():
    return TransferReader().take_def_transactions()
    