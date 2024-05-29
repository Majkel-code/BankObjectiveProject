import json
from pathlib import Path

import yaml

from users.transfers.transfer_maker import TransferMaker


class CreditConstruct:
    def __init__(self) -> None:
        """
        Initializes a new instance of the CreditConstruct class.

        This constructor sets up the necessary attributes for the CreditConstruct class. It initializes the following attributes:
        - `path`: The absolute path to the parent directory of the current file, level up twice.
        - `credit_path`: The path to the credit data directory, which is located in the `users/credits` directory of the parent directory of the current file, level up twice.
        - `credit_file`: An empty dictionary representing the credit file.
        - `credit_struc`: A dictionary representing the structure of a credit object, with the following keys:
            - `ID`: The ID of the credit.
            - `NAME`: The name of the borrower.
            - `L_NAME`: The last name of the borrower.
            - `START_DATE`: The start date of the credit.
            - `CREDIT_AMOUNT`: The total amount of the credit.
            - `CREDIT_MONTHLY`: The monthly payment of the credit.
            - `CREDIT_INTEREST`: The interest rate of the credit.
            - `END_DATE`: The end date of the credit.
            - `SCHEDULE`: An empty list representing the payment schedule of the credit.

        Args:
        - None

        Returns:
        - None
        """
        self.path = Path(__file__).absolute().parents[2]
        self.credit_path = f"{self.path}/users/credits/credit_data"
        self.credit_file = {"credits": []}
        self.credit_struc = {
            "ID": None,
            "NAME": None,
            "L_NAME": None,
            "START_DATE": None,
            "CREDIT_AMOUNT": None,
            "CREDIT_MONTHLY": None,
            "CREDIT_INTEREST": None,
            "END_DATE": None,
            "SCHEDULE": [],
        }

    def load_credit_config(self):
        """
        Load the credit configuration from a YAML file.

        Returns:
            dict: The parsed YAML object representing the credit configuration.

        Raises:
            FileNotFoundError: If the specified YAML file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        with open(f"{self.path}/configs/config_files/credits_config.yaml", "r") as f:
            return yaml.safe_load(f)

    def create_credit_file(self, id):
        """
        Creates a credit file for a given user ID.

        Args:
            id (str): The ID of the user for whom the credit file is being created.

        Returns:
            dict: A dictionary containing the status of the credit file creation process.

                - - "STATUS" (bool): Indicates whether the credit file was successfully created.
                - - "ERROR" (str or None): If the credit file creation was unsuccessful, this key contains an error message. Otherwise, it is None.
                - - "DATA" (str or None): If the credit file creation was unsuccessful, this key contains the error message. Otherwise, it is None.

        Raises:
            Exception: If there is an error while saving the credit file.
        """
        try:
            with open(f"{self.credit_path}/{id}.json", "a") as f:
                f.write(json.dumps(self.credit_file))
            return {"STATUS": True, "ERROR": None, "DATA": None}
        except Exception as e:
            return {"STATUS": False, "ERROR": "Unabe to save credit data!", "DATA": e}

    def edit_credit_file(self, id):
        """
        Edit the credit file for a given user ID.

        Args:
            id (str): The ID of the user for whom the credit file is being edited.

        Returns:
            dict: A dictionary containing the status of the credit file editing process.

                - "STATUS" (bool): Indicates whether the credit file was successfully edited.
                - "ERROR" (str or None): If the credit file editing was unsuccessful, this key contains an error message. Otherwise, it is None.
                - "DATA" (str or None): If the credit file editing was unsuccessful, this key contains the error message. Otherwise, it is None.

        Raises:
            Exception: If there is an error while saving the credit file.
        """
        try:
            with open(f"{self.credit_path}/{id}.json", "w") as f:
                json.dump(self.credit_file, f)
            return {"STATUS": True, "ERROR": None, "DATA": None}
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to save credit data!", "DATA": e}

    def add_credit_amount_to_account(self, id, data):
        """
        Adds the credit amount to the user's account.

        Args:
            id (str): The ID of the user.
            data (dict): The data containing the credit amount.

        Returns:
            dict: The result of saving the credit income.

        Raises:
            Exception: If there is an error while saving the credit income.
        """
        return TransferMaker().credit_income_save(id, **data)

    def calculate_excess_credit(self, id, data):
        """
        Calculates the excess credit for a user.

        Args:
            id (str): The ID of the user.
            data (dict): The data containing the credit amount.

        Returns:
            dict: The result of saving the credit outcome.

        Raises:
            Exception: If there is an error while saving the credit outcome.
        """
        return TransferMaker().credit_outcome_save(id, **data)
