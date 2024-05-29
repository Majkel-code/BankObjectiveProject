from fastapi import APIRouter, Body

from users.user_authorization.authorize_registry.auth_registry import RegistryAuthorization

router = APIRouter(
    prefix="/register",
)


@router.put("/")
async def receive_data(data: dict = Body(...)):
    """
    This function receives a dictionary `data` containing user registration data.

    Parameters:
        data (dict): A dictionary containing user registration data.

    Returns:
        dict: A dictionary with the following keys:

            - "STATUS" (bool): Indicates whether the registration was successful.
            - "ERROR" (str or None): If the registration was not successful, this key contains an error message. Otherwise, it is None.
            - "DATA" (dict or None): If the registration was successful, this key contains the registered user's data. Otherwise, it is None.
    """
    register_authorization = RegistryAuthorization()
    if register_authorization.check_user_exist(pesel=data.get("pesel"))["STATUS"]:
        return register_authorization.register_user(**data)
    else:
        return {"STATUS": False, "ERROR": "Taki urzytkownik istnieje!", "DATA": None}
