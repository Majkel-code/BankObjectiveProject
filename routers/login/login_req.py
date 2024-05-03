from fastapi import APIRouter, Body
from users.user_authorization.authorize_login.auth_login import LoginAuthorization
# from pydantic import BaseModel

# class Structure(BaseModel):
#     data1: str
#     # data2: str | int | float

router = APIRouter(
    prefix="/login",
)


@router.put("/")
async def receive_data(data: dict = Body(...)):
    print(data)
    username = data.get("acc_id")
    password = data.get("password")
    print(username, password)
    login_authorization = LoginAuthorization().check_login_data(username,password)
    print(login_authorization)
    if login_authorization["STATUS"]:
        return login_authorization
    else:
        return login_authorization
    
    
