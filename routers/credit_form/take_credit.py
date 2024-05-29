from fastapi import APIRouter, Body

from configs.config_returner import ConfigReturner
from users.credits.credit_maker import CreditMaker
from users.credits.credit_reader import CreditReader

router = APIRouter(
    prefix="/credit",
)


@router.get("/costs")
async def send_data():
    """
    Retrieves the credit costs by calling the `credit_config_returner` method of the `ConfigReturner` class.

    Returns:
        dict: A dictionary containing the credit costs. The dictionary has the following keys:

            - "STATUS" (bool): Indicates whether the retrieval was successful.
            - "ERROR" (str or None): If the retrieval was not successful, this key contains an error message. Otherwise, it is None.
            - "DATA" (dict or None): If the retrieval was successful, this key contains the credit costs. Otherwise, it is None.
    """
    return ConfigReturner().credit_config_returner()


@router.post("/new")
async def new_credit(data: dict = Body(...)):
    """
    Creates a new credit by calling the `setup_credit_calculation` method of the `CreditMaker` class with the provided data.

    Args:
        data (dict): The data required to calculate the credit.

    Returns:
        The result of the credit calculation.

            - "STATUS" (bool): Indicates whether the operation was successful.
            - "ERROR" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.
            - "DATA" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.
    """
    return CreditMaker().setup_credit_calculation(**data)


@router.patch("/havecredit")
async def check_credit(data: dict = Body(...)):
    """
    Check if a credit exists for a given account ID.

    Parameters:
        data (dict): The request body containing the account ID.
            - "acc_id" (str): The account ID to check for a credit.

    Returns:
        dict: The credit data for the account ID, if it exists.

            - "STATUS" (bool): Indicates whether the credit data was found.
            - "ERROR" (str or None): If the credit data was not found, this key contains an error message. Otherwise, it is None.
            - "DATA" (dict or None): If the credit data was found, this key contains the credit data. Otherwise, it is None.
    """
    return CreditReader().return_credit_data(data["acc_id"])
