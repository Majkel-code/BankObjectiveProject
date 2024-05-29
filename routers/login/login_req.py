from fastapi import APIRouter, Body

from users.user_authorization.authorize_login.auth_login import LoginAuthorization
from users.user_authorization.user_reader import UsersReader

router = APIRouter(
    prefix="/login",
)


@router.put("/")
async def receive_data(data: dict = Body(...)):
    """
    Receive data from the client and check if the login credentials are valid.

    Parameters:
        data (dict): The data received from the client. It should contain the following keys:
            - "acc_id" (str): The username or account ID.
            - "password" (str): The password.

    Returns:
        dict: A dictionary containing the login authorization status. The dictionary has the following structure:

            - "STATUS" (bool): Indicates whether the login credentials are valid.
            - "ERROR" (str or None): If "STATUS" is False, this field contains an error message. Otherwise, it is None.
            - "DATA" (dict or None): If "STATUS" is True, this field contains additional data related to the login. Otherwise, it is None.
    """
    username = data.get("acc_id")
    password = data.get("password")
    login_authorization = LoginAuthorization().check_login_data(username, password)
    if login_authorization["STATUS"]:
        return login_authorization
    else:
        return login_authorization


@router.patch("/take_data")
async def take_data(data: dict = Body(...)):
    """
    A function that takes data from the client and retrieves user data based on the provided account ID.

    Parameters:
        - data (dict): The data received from the client. It should contain the following keys:
            - "acc_id" (str): The account ID of the user.

    Returns:
        - dict: A dictionary containing the user data. The dictionary has the following structure:

            - "STATUS" (bool): Indicates whether the user data was successfully retrieved.
            - "ERROR" (str or None): If "STATUS" is False, this field contains an error message. Otherwise, it is None.
            - "DATA" (dict or None): If "STATUS" is True, this field contains the user data. Otherwise, it is None.
    """
    return UsersReader().take_user_data(id=data.get("acc_id"))
