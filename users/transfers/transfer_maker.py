import json
import os
from pathlib import Path

from users.user_authorization.user_reader import UsersReader


class TransferMaker:
    def __init__(self) -> None:
        """
        Initializes a new instance of the TransferMaker class.

        This constructor sets up the necessary attributes for the TransferMaker class.
        It initializes the following attributes:
        - `path`: The absolute path to the parent directory of the current file, level up one.
        - `history_path`: The path to the history directory for transfers, which is
        located in the `transfers/transfer_data` directory of the parent directory of
        the current file, level up one.
        - `receiver_to_save`: A dictionary representing the receiver's history, with an
        empty "history" list.
        - `transfers_path`: The path to the transfers directory for transfers, which
        is located in the `transfers/transfer_data` directory of the parent directory
        of the current file, level up one.
        - `transfers_file`: A dictionary representing the transfers file, with an
        empty "transfers" list.
        - `to_save`: A dictionary representing the transfers to be saved, with an
        empty "transfers" list.
        - `transfer_struc`: A dictionary representing the structure of a transfer object,
        with the following keys:
            - "FROM_ACC": None
            - "SENDER": None
            - "TO_ACC": None
            - "RECEIVER": None
            - "AMOUNT": None
            - "DATE": None
            - "TIME": None
            - "TITLE": None
            - "DESC": None

        Args:
        - None

        Returns:
        - None
        """

        self.path = Path(__file__).absolute().parents[1]
        self.history_path = f"{self.path}/transfers/transfer_data/history"
        self.receiver_to_save = {"history": []}
        self.transfers_path = f"{self.path}/transfers/transfer_data/transfers"
        self.transfers_file = {"transfers": []}
        self.to_save = {"transfers": []}
        self.transfer_struc = {
            "FROM_ACC": None,
            "SENDER": None,
            "TO_ACC": None,
            "RECEIVER": None,
            "AMOUNT": None,
            "DATE": None,
            "TIME": None,
            "TITLE": None,
            "DESC": None,
        }

    def setup_files(self, user):
        """
        Set up the files for a given user.

        Args:
            user (str): The ID of the user.

        Returns:
            dict: A dictionary containing the following keys:

                - "STATUS" (bool): Indicates whether the files were successfully set up.
                - "ERROR" (str or None): An error message if the files could not be set up, otherwise None.
                - "DATA" (None): Always None.

        """

        if os.path.exists(f"{self.transfers_path}/{user}.json"):
            with open(f"{self.transfers_path}/{user}.json", "r") as f:
                self.transfers_file = json.load(f)
            return {"STATUS": True, "ERROR": None, "DATA": None}
        return {"STATUS": False, "ERROR": "Unable to setup file!", "DATA": None}

    def create_file(self, user):
        """
        Create a file for a given user.

        Args:
            user (str): The ID of the user.

        Returns:
            dict: A dictionary containing the following keys:

                    - "STATUS" (bool): Indicates whether the file was successfully created.
                    - "ERROR" (str or None): An error message if the file could not be created, otherwise None.
                    - "DATA" (str or None): The exception message if an error occurred, otherwise None.
        """
        try:
            with open(f"{self.transfers_path}/{user}.json", "a") as f:
                f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None}
        except Exception as e:
            return {"STATUS": False, "ERROR": "Unable to create file!", "DATA": e}

    def find_accounts(self, id: int = None):
        """
        Finds accounts based on the given parameters.

        Args:
            id (int, optional): The ID of the user. If provided, the account will be found based on the ID.

        Returns:
            dict: A dictionary with the following keys:

                    - - "STATUS" (bool): True if the account was found, False otherwise.

                    - - "ERROR" (str or None): An error message if the account was not found, or None otherwise.

                    - - "DATA" (dict or None): A dictionary with the account details if the account was found, None otherwise.
        """
        if id is not None:
            return UsersReader().find_account(
                to_acc_num=None,
                from_acc_num=None,
                amount=self.transfer_struc["AMOUNT"],
                id=id,
            )
        else:
            return UsersReader().find_account(
                to_acc_num=self.transfer_struc["TO_ACC"],
                from_acc_num=self.transfer_struc["FROM_ACC"],
                amount=self.transfer_struc["AMOUNT"],
            )

    def find_user_id(self, acc_num):
        """
        Finds the user ID based on the account number.

        Args:
            acc_num (str): The account number to search for.

        Returns:
            dict: A dictionary containing the user ID if found, or an error message if not found.
                The dictionary has the following structure:

                {
                    "STATUS": bool,
                    "ERROR": str or None,
                    "DATA": str or None
                }

                - "STATUS": True if the user ID is found, False otherwise.
                - "ERROR": None if the user ID is found, or an error message if not found.
                - "DATA": The user ID if found, or None if not found.
        """
        return UsersReader().find_id(acc_num=acc_num)

    def income_path_user(self, finded_user_income):
        """
        Check if the income path for a user exists.

        Args:
            finded_user_income (dict): A dictionary containing the user information.
                It should have the following structure:

                {
                    "STATUS": bool,
                    "ERROR": str or None,
                    "DATA": { "ID" : str }
                }

        Returns:
            bool: True if the income path exists, False otherwise.

        Raises:
            Exception: If there is an error while checking the income path.
        """
        try:
            if os.path.exists(f"{self.transfers_path}/{finded_user_income['DATA']['ID']}.json"):
                return True
        except Exception:
            return False

    def outcome_path_user(self, finded_user_outcome):
        """
        Check if the outcome path for a user exists.

        This function takes in a dictionary `finded_user_outcome` and checks if the corresponding JSON file exists in the `transfers_path` directory. The function returns `True` if the file exists and `False` otherwise.

        Args:
            finded_user_outcome (dict): A dictionary containing the user information. It should have the following structure:
                {
                    "DATA": str  # The name of the user
                }

        Returns:
            bool: True if the outcome path exists, False otherwise.
        """
        try:
            if os.path.exists(f"{self.transfers_path}/{finded_user_outcome['DATA']}.json"):
                return True
        except Exception:
            return False

    def setup_history_path(self, user, file):
        """
        Set up the history path for a user.

        This function checks if the JSON file for the specified user exists in the `history_path` directory. If the file exists, it reads the contents of the file and returns the loaded data. If the file does not exist, it returns `False`.

        Args:
            user (str): The name of the user.
            file (dict): An empty dictionary to store the loaded data.

        Returns:
            dict or bool: The loaded data if the file exists, `False` otherwise.
        """
        if os.path.exists(f"{self.history_path}/{user}.json"):
            with open(f"{self.history_path}/{user}.json", "r") as f:
                file = json.load(f)
            return file
        return False

    def save_to_history(self, id):
        """
        Save the first transfer from the `transfers_file` to the history file for the specified user.

        Parameters:
            id (str): The ID of the user.

        Returns:
            None

        Note:
            - This function assumes that the `setup_files` method is implemented and returns a dictionary with a `STATUS` key.
            - This function assumes that the `transfers_file` and `history_path` attributes are properly initialized and contain valid values.
        """
        if id is not None:
            if self.setup_files(user=id)["STATUS"]:
                if len(self.transfers_file["transfers"]) >= 3:
                    if os.path.exists(f"{self.history_path}/{id}.json"):
                        with open(f"{self.history_path}/{id}.json", "r") as f:
                            self.receiver_to_save = json.load(f)
                    else:
                        with open(f"{self.history_path}/{id}.json", "a") as f:
                            f.write(json.dumps(self.receiver_to_save))
                    self.receiver_to_save["history"].append(self.transfers_file["transfers"][0])
                    del self.transfers_file["transfers"][0]

                    with open(f"{self.transfers_path}/{id}.json", "w") as f:
                        json.dump(self.transfers_file, f)

                    with open(f"{self.history_path}/{id}.json", "r+") as f:
                        f.write(json.dumps(self.receiver_to_save))

    def other_bank_user(self):
        """
        Check if the file for a different bank user exists and register a transfer if it does.


        Returns:
            dict: A dictionary with the keys "STATUS" (bool), "ERROR" (str or None), and "DATA" (str or None).
        """
        if os.path.exists(f"{self.transfers_path}/differentBank.json"):
            try:
                with open(f"{self.transfers_path}/differentBank.json", "r+") as f:
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None, "DATA": None}
            except Exception as e:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!", "DATA": e}
        else:
            with open(f"{self.transfers_path}/differentBank.json", "a") as f:
                f.write(json.dumps(self.transfers_file))

    def save_outcome(self, user_sender, amount):
        """
        Save the outcome of a transfer to the user's file.

        Args:
            user_sender (int): The ID of the user who sent the transfer.
            amount (float): The amount of the transfer.

        Returns:
            dict: A dictionary with the keys:

                    - "STATUS" (bool):
                        - Indicates whether the operation was successful.
                    - "ERROR" (str or None):
                        - If the operation was not successful, this key contains an error message. Otherwise, it is None.
                    - "DATA" (dict):
        """
        user_id = user_sender
        self.transfer_struc["AMOUNT"] = -amount
        self.to_save["transfers"].append(self.transfer_struc)
        if self.setup_files(user=user_id)["STATUS"]:
            try:
                with open(f"{self.transfers_path}/{user_id}.json", "r+") as f:
                    self.transfers_file["transfers"].append(self.transfer_struc)
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None, "DATA": None}
            except Exception as e:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!", "DATA": e}
        else:
            with open(f"{self.transfers_path}/{user_id}.json", "a") as f:
                f.write(json.dumps(self.to_save))

    def save_income(self, user):
        """
        Saves the income of a user to a JSON file.

        Args:
            user (int): The ID of the user whose income is being saved.

        Returns:
            dict: A dictionary with the keys:

                    - "STATUS" (bool):
                        - Indicates whether the operation was successful.
                    - "ERROR" (str or None):
                        - If the operation was not successful, this key contains an error message. Otherwise, it is None.
                    - "DATA" (dict):
                        - The loaded default transactions data.

        """
        if self.setup_files(user)["STATUS"]:
            try:
                with open(f"{self.transfers_path}/{user}.json", "r+") as f:
                    self.transfers_file["transfers"].append(self.transfer_struc)
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None, "DATA": None}
            except Exception as e:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!", "DATA": e}
        else:
            self.transfers_file["transfers"].append(self.transfer_struc)
            return self.create_file(user=user)

    def credit_income_save(self, id: int, **kwargs):
        """
        Saves the credit income for a user.

        Args:
            id (int): The ID of the user.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary with the keys:

                    - "STATUS" (bool):
                        - Indicates whether the operation was successful.
                    - "ERROR" (str or None):
                        - If the operation was not successful, this key contains an error message. Otherwise, it is None.
                    - "DATA" (dict):
                        - The loaded default transactions data.

        Raises:
            Exception: If there is an error while saving the credit income.

        """
        self.transfer_struc = kwargs
        finded_user_income = self.find_accounts(id)
        if self.income_path_user(id):
            self.save_to_history(
                id=id,
            )
        try:
            self.save_income(user=finded_user_income['DATA']["ID"])
            return UsersReader().return_user_amount(id=id)
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to register credit transfer!", "DATA": e}

    def perform_outcome(self, id, send_money):
        """
        Calculates the outgoing balance for a user based on their ID and the amount of money being sent.

        Args:
            id (int): The ID of the user.
            send_money (float): The amount of money being sent.

        Returns:
            None
        """
        UsersReader().calculate_outcoming_balance(acc_num=None, send_money=send_money, id=id)

    def credit_outcome_save(self, id: int, **kwargs):
        """
        Saves the credit outcome for a user.

        Args:
            id (int): The ID of the user.
            **kwargs: Additional keyword arguments.

                    - "sender" (str): The sender of the credit transfer.
                    - "from_acc" (str): The account number of the sender.
                    - "to_acc" (str): The account number of the receiver.
                    - "amount" (float): The amount of the credit transfer.
                    - "date" (str): The date of the credit transfer.
                    - "time" (str): The time of the credit transfer.
                    - "title" (str): The title of the credit transfer.
                    - "desc" (str): The description of the credit transfer.

        Returns:
            dict: A dictionary with the keys:

                    - "STATUS" (bool): Indicates whether the operation was successful.
                    - "ERROR" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.
                    - "DATA" (dict): The loaded default transactions data.

        Raises:
            Exception: If there is an error while saving the credit outcome.

        """
        self.transfer_struc["SENDER"] = kwargs["sender"]
        self.transfer_struc["RECEIVER"] = "CoronaBank S.A."
        self.transfer_struc["FROM_ACC"] = str(kwargs["from_acc"])
        self.transfer_struc["TO_ACC"] = kwargs["to_acc"]
        self.transfer_struc["AMOUNT"] = kwargs["amount"]
        self.transfer_struc["DATE"] = kwargs["date"]
        self.transfer_struc["TIME"] = kwargs["time"]
        self.transfer_struc["TITLE"] = kwargs["title"]
        self.transfer_struc["DESC"] = kwargs["desc"]
        amount = kwargs["amount"]
        self.transfer_struc["AMOUNT"] = -amount

        if self.income_path_user(id):
            self.save_to_history(
                id=id,
            )
        try:
            self.save_outcome(user_sender=id, amount=kwargs["amount"])
            self.perform_outcome(id=id, send_money=kwargs["amount"])
            return UsersReader().return_user_amount(id=id)
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to register credit transfer!", "DATA": e}

    def save_transfer(self, **kwargs):
        """
        Saves a transfer to the transfer_struc dictionary and performs additional operations based on the transfer details.

        Args:
            **kwargs: A dictionary of keyword arguments containing the following keys:

                - "company" (str): The receiver of the transfer (optional).
                - "sender" (str): The sender of the transfer.
                - "from_acc" (str): The senders account number.
                - "to_acc" (str): The receivers account number.
                - "amount" (float): The amount of the transfer.
                - "date" (str): The date of the transfer.
                - "time" (str): The time of the transfer.
                - "title" (str): The title of the transfer.
                - "desc" (str): The description of the transfer.

        Returns:
            dict: A dictionary with the keys:

                - "STATUS" (bool): Indicates whether the transfer was successfully registered.
                - "ERROR" (str or None): If the transfer was not registered successfully, this key contains an error message. Otherwise, it is None.
                - "DATA" (dict): The user amount returned by ``UsersReader().return_user_amount()``.

        Raises:
            Exception: If there is an error while saving the transfer or performing additional operations.
        """
        if kwargs["company"] != '':
            self.transfer_struc["RECEIVER"] = kwargs["company"]
        self.transfer_struc["SENDER"] = kwargs["sender"]
        self.transfer_struc["FROM_ACC"] = str(kwargs["from_acc"])
        self.transfer_struc["TO_ACC"] = kwargs["to_acc"]
        self.transfer_struc["AMOUNT"] = kwargs["amount"]
        self.transfer_struc["DATE"] = kwargs["date"]
        self.transfer_struc["TIME"] = kwargs["time"]
        self.transfer_struc["TITLE"] = kwargs["title"]
        self.transfer_struc["DESC"] = kwargs["desc"]

        finded_user_income = self.find_accounts()
        finded_user_outcome = self.find_user_id(self.transfer_struc["FROM_ACC"])

        if self.income_path_user(finded_user_income):
            self.save_to_history(
                id=finded_user_income['DATA']["ID"],
            )
        if self.outcome_path_user(finded_user_outcome):
            self.save_to_history(
                id=finded_user_outcome['DATA'],
            )
        try:
            if finded_user_income["STATUS"]:
                self.transfer_struc["RECEIVER"] = finded_user_income['DATA']["RECEIVER"]
                self.save_income(user=finded_user_income['DATA']["ID"])
            else:
                self.transfers_file["transfers"].append(self.transfer_struc)
                self.other_bank_user()
            self.save_outcome(user_sender=finded_user_outcome["DATA"], amount=kwargs["amount"])
            return UsersReader().return_user_amount(finded_user_outcome['DATA'])
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to register transfer!", "DATA": e}
