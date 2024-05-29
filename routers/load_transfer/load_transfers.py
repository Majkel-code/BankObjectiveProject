from fastapi import APIRouter, Body

from users.credits.credit_maker import CreditMaker
from users.transfers.transfer_maker import TransferMaker
from users.transfers.transfer_reader import TransferReader

router = APIRouter(
    prefix="/transfers",
)


@router.post("/last_history")
async def receive_data(data: dict = Body(...)):
    """
    Receive data from the client and check the last transfer history of a user.

    Parameters:
        data (dict): A dictionary containing the user's account ID.
            - "acc_id" (str): The account ID of the user.

    Returns:
        dict: A dictionary containing the transfer history of the user.

            - "STATUS" (bool): Indicates whether the operation was successful.
            - "ERROR" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.
            - "DATA" (dict or None): The loaded transfer history data. If the operation was successful, the data is a dictionary with the following keys:

    NOTES:
        - - The first key of the input dictionary (obtained using `self.take_dict_key(data)[0]`).
        - - The last 3 transfers in reverse order (obtained using `data["transfers"][-3:][::-1]`).
        - - If the operation was not successful, the data is None.
    """
    return TransferReader().check_history(data.get("acc_id"))


@router.post("/newtransfer")
async def new_transfer(data: dict = Body(...)):
    """
    Endpoint for creating a new transfer.

    This function receives a dictionary of transfer data from the client via a POST request. The data dictionary should contain the following keys:

            - "to_acc" (str): The recipient's account number.
            - "amount" (float): The amount of the transfer.
            - Additional keys may be present depending on the specific implementation of the CreditMaker and TransferMaker classes.

    If the recipient's account number is equal to "9999 9999 9999 9999", the function calls the `setup_credit_calculation` method of the `CreditMaker` class with the excess amount and the operation set to "EXCESS". The remaining keys from the data dictionary are passed as keyword arguments.

    If the recipient's account number is not equal to "9999 9999 9999 9999", the function calls the `save_transfer` method of the `TransferMaker` class with the data dictionary passed as keyword arguments.

    Returns:
        - - The return value of the `setup_credit_calculation` method if the recipient's account number is equal to "9999 9999 9999 9999".
        - - The return value of the `save_transfer` method if the recipient's account number is not equal to "9999 9999 9999 9999".
    """
    if data["to_acc"] == "9999 9999 9999 9999":
        return CreditMaker().setup_credit_calculation(
            excess_amount=data["amount"], operation="EXCESS", **data
        )
    return TransferMaker().save_transfer(**data)


@router.get("/defoult")
async def get_defoult():
    """
    Retrieves the default transactions from the TransferReader class.

    This function is an asynchronous handler for the GET request to the "/defoult" endpoint. It calls the `take_def_transactions` method of the `TransferReader` class to retrieve the default transactions.

    Returns:
        The result of the `take_def_transactions` method, which is a dictionary containing the following keys:

            - "STATUS" (bool): Indicates whether the operation was successful.
            - "ERROR" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.
            - "DATA" (dict): The loaded default transactions data.

    """
    return TransferReader().take_def_transactions()
