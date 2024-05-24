from fastapi import APIRouter, Body
from users.credits.credit_maker import CreditMaker
from users.credits.credit_reader import CreditReader
from configs.config_returner import ConfigReturner

router = APIRouter(
    prefix="/credit",
)

@router.get("/costs")
async def send_data():
    return ConfigReturner().credit_config_returner()


@router.post("/new")
async def new_credit(data: dict = Body(...)):
    return CreditMaker().setup_credit_calculation(**data)


@router.patch("/havecredit")
async def check_credit(data: dict = Body(...)):
    return CreditReader().return_credit_data(data["acc_id"])