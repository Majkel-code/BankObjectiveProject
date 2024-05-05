from fastapi import APIRouter, Body
from users.user_authorization.authorize_registry.auth_registry import RegistryAuthorization
# from pydantic import BaseModel

# class Structure(BaseModel):
#     data1: str
#     # data2: str | int | float

router = APIRouter(
    prefix="/register",
)


@router.put("/")
async def receive_data(data: dict = Body(...)):
    register_authorization = RegistryAuthorization()
    if register_authorization.check_user_exist(pesel=data.get("pesel"))["STATUS"]:
        return register_authorization.register_user(**data)
    else:
        return {"STATUS": False, "ERROR": "Taki urzytkownik istnieje!"}
    