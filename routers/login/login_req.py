from fastapi import APIRouter, Body

from users.user_authorization.authorize_login.auth_login import LoginAuthorization
from users.user_authorization.user_reader import UsersReader

router = APIRouter(
    prefix="/login",
)


@router.put("/")
async def receive_data(data: dict = Body(...)):
    username = data.get("acc_id")
    password = data.get("password")
    login_authorization = LoginAuthorization().check_login_data(username, password)
    if login_authorization["STATUS"]:
        return login_authorization
    else:
        return login_authorization


@router.patch("/take_data")
async def take_data(data: dict = Body(...)):
    return UsersReader().take_user_data(id=data.get("acc_id"))
