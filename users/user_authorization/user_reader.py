import json
import os
from pathlib import Path


class UsersReader:
    def __init__(self) -> None:
        """
        Initializes a new instance of the UsersReader class.

        This constructor sets up the necessary attributes for the UsersReader class. It initializes
        the following attributes:
        - `users_path`: The absolute path to the parent directory of the current file, level up
        twice.
        - `registry_path`: The path to the users registry file, which is located in the
        `users/user_data` directory of the parent directory of the current file, level up twice.
        - `registry_file`: An empty dictionary representing the users registry file.
        - `def_user`: A default user object with predefined values for various attributes.
        - `registry_struc`: A dictionary representing the structure of a user object in the
        registry file.

        The constructor also calls the `setup_files` method to ensure that the necessary files are
        set up correctly.

        Parameters:
        - None

        Returns:
        - None
        """
        self.users_path = Path(__file__).absolute().parents[2]
        self.registry_path = f"{self.users_path}/users/user_data/users_registry.json"
        self.registry_file = {"users": []}
        self.def_user = {
            "users": [
                {
                    "ID": "99999",
                    "ACC_NUM": "4444 4444 4444 4444",
                    "PASSWORD": "testpassword",
                    "NAME": "Test",
                    "L_NAME": "Test",
                    "E_MAIL": "testmail@test.com",
                    "PESEL": "99999999999",
                    "ACC_BALANSE": 500,
                }
            ]
        }
        self.registry_struc = {
            "ID": None,
            "ACC_NUM": None,
            "PASSWORD": None,
            "NAME": None,
            "L_NAME": None,
            "E_MAIL": None,
            "PESEL": None,
            "ACC_BALANSE": 500,
        }
        self.setup_files()

    def setup_files(self):
        """
        Set up the necessary files for the UsersReader class.

        This function checks if the registry file exists at the specified path. If it does,
        it opens the file and loads its contents into the `registry_file` attribute.
        If the file does not exist, it calls the `create_file` method to create the file.

        Args:
            None

        Returns:
            None
        """
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r") as f:
                self.registry_file = json.load(f)
        else:
            self.create_file()

    def find_id(self, acc_num):
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
        for user in self.registry_file["users"]:
            if acc_num == user["ACC_NUM"]:
                return {"STATUS": True, "ERROR": None, "DATA": user["ID"]}
        return {"STATUS": False, "ERROR": "Unabe to find user data!", "DATA": None}

    def take_user_data(self, id):
        """
        Retrieves user data based on the provided ID.

        Args:
            id (int): The ID of the user.

        Returns:
            dict: A dictionary containing the user data if found, or an error message if not found. The dictionary has the following structure:
                {
                    "STATUS": bool,
                    "ERROR": str or None,
                    "DATA": dict or None
                }

                - "STATUS": True if the user data is found, False otherwise.
                - "ERROR": None if the user data is found, or an error message if not found.
                - "DATA": The user data if found, or None if not found.
        """
        for user in self.registry_file["users"]:
            if user["ID"] == id:
                return {"STATUS": True, "ERROR": None, "DATA": user}
        return {"STATUS": False, "ERROR": "Unabe to find user data!", "DATA": None}

    def return_user_amount(self, id):
        """
        Returns the account balance of a user based on their ID.

        Args:
            id (int): The ID of the user.

        Returns:
            dict: A dictionary containing the account balance if found, or an error message if not found. The dictionary has the following structure:
                {
                    "STATUS": bool,
                    "ERROR": str or None,
                    "DATA": float or None
                }

                - "STATUS": True if the account balance is found, False otherwise.
                - "ERROR": None if the account balance is found, or an error message if not found.
                - "DATA": The account balance if found, or None if not found.
        """
        for user in self.registry_file["users"]:
            if id == user["ID"]:
                return {"STATUS": True, "ERROR": None, "DATA": user["ACC_BALANSE"]}
        return {"STATUS": False, "ERROR": "Unabe to find user data!", "DATA": None}

    def calculate_incoming_balance(self, record, send_money):
        """
        Calculates the incoming balance for a user by adding the `send_money`
        amount to the `ACC_BALANSE` field of the `record` dictionary.

        Args:
            record (dict): A dictionary representing a user record. It should have the following keys:

                        - "ID" (int): The ID of the user.
                        - "ACC_BALANSE" (float): The current balance of the user.
                        - "NAME" (str): The first name of the user.
                        - "L_NAME" (str): The last name of the user.

               send_money (float): The amount to be added to the user's balance.

        Returns:
            dict: The dictionary has the following structure:

                {
                    "STATUS": bool,
                    "ERROR": str or None,
                    "DATA": dict or None
                }

                - "STATUS" (bool): True if the balance was successfully calculated and updated, False otherwise.
                - "ERROR" (str or None): None if the balance was successfully calculated and updated, or an error message if not.
                - "DATA" (dict or None): A dictionary with the following keys if the balance was successfully calculated and updated:
                    - "ID" (int): The ID of the user.
                    - "RECEIVER" (str): The full name of the user.

        """
        record["ACC_BALANSE"] = record["ACC_BALANSE"] + send_money
        for user_data in self.registry_file["users"]:
            if user_data["ID"] == record["ID"]:
                try:
                    with open(self.registry_path, "r+") as f:
                        f.write(json.dumps(self.registry_file))
                    return {
                        "STATUS": True,
                        "ERROR": None,
                        "DATA": {
                            "ID": record["ID"],
                            "RECEIVER": f'{record["NAME"]} {record["L_NAME"]}',
                        },
                    }
                except Exception as e:
                    return {"STATUS": False, "ERROR": "Unabe to calculate balance!", "DATA": e}

    def calculate_outcoming_balance(self, acc_num, send_money, id: int = None):
        """
        Calculates the outgoing balance for a user based on their ID or account number.

        Args:
            acc_num (int): The account number of the user.
            send_money (float): The amount of money being sent out.
            id (int, optional): The ID of the user. If provided,
            the balance will be calculated based on the ID.

        Returns:
            dict: A dictionary with the following keys if the balance was successfully calculated and updated:

                    - "STATUS" (bool):
                        - True if the balance was successfully calculated and updated, False otherwise.
                    - "ERROR" (str):
                        - None if the balance was successfully calculated and updated, or an error message otherwise.
                    - "DATA" (int):
                        - The ID of the user if the balance was successfully calculated and updated.

        """
        if id is not None:
            for record in self.registry_file["users"]:
                if record["ID"] == id:
                    record["ACC_BALANSE"] = record["ACC_BALANSE"] - send_money
                    try:
                        with open(self.registry_path, "r+") as f:
                            f.write(json.dumps(self.registry_file))
                        return {"STATUS": True, "ERROR": None, "DATA": record["ID"]}
                    except Exception as e:
                        return {"STATUS": False, "ERROR": "Unabe to calculate balance!", "DATA": e}
        for record in self.registry_file["users"]:
            if record["ACC_NUM"] == acc_num:
                record["ACC_BALANSE"] = record["ACC_BALANSE"] - send_money
                try:
                    with open(self.registry_path, "r+") as f:
                        f.write(json.dumps(self.registry_file))
                    return {"STATUS": True, "ERROR": None, "DATA": record["ID"]}
                except Exception as e:
                    return {"STATUS": False, "ERROR": "Unabe to calculate balance!", "DATA": e}

    def find_account(self, to_acc_num, from_acc_num, amount, id: int = None):
        """
        Finds an account based on the given parameters.

        Args:
            to_acc_num (int): The account number of the receiver.
            from_acc_num (int): The account number of the sender.
            amount (float): The amount to be transferred.
            id (int, optional): The ID of the user. If provided, the account will be found
            based on the ID.

        Returns:
            dict: A dictionary with the following keys:

                    - "STATUS" (bool): True if the account was found, False otherwise.

                    - "ERROR" (str or None): An error message if the account was not found, or None otherwise.

                    - "DATA" (dict or None): A dictionary with the account details if the account was
                    found, None otherwise.

        """
        self.setup_files()
        if id is not None:
            for record in self.registry_file["users"]:
                if record["ID"] == id:
                    return self.calculate_incoming_balance(record=record, send_money=amount)
        self.calculate_outcoming_balance(acc_num=from_acc_num, send_money=amount)
        for record in self.registry_file["users"]:
            if record["ACC_NUM"] == to_acc_num:
                return self.calculate_incoming_balance(record=record, send_money=amount)
        return {"STATUS": False, "ERROR": "There is no account", "DATA": None}

    def create_file(self):
        """
        Creates a new file at the specified registry path and writes the default user data in
        JSON format to the file.

        This function does not take any args.

        Returns:
            None
        """
        with open(self.registry_path, "a") as f:
            f.write(json.dumps(self.def_user))

    def acc_num_separator(self, number):
        """
        Separates a given number into groups of four digits and returns them as a string
        with spaces between each group.

        Parameters:
            number (str): The number to be separated.

        Returns:
            str: The separated number with spaces between each group.
        """
        return " ".join([number[i : i + 4] for i in range(0, len(number), 4)])

    def save_user_data(self, **kwargs):
        """
        Saves user data to the registry file.

        Args:
            acc_id (int): The account ID.
            acc_number (str): The account number.
            password (str): The user's password.
            name (str): The user's first name.
            surname (str): The user's last name.
            email (str): The user's email address.
            pesel (str): The user's PESEL number.

        Returns:
            dict: A dictionary with the following keys:

                - "STATUS" (bool): Indicates whether the operation was successful.

                - "ERROR" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.

                - "DATA" (str): The user's ID.

        Raises:
            Exception: If an error occurs during the operation.
        """
        self.registry_struc["ID"] = str(kwargs["acc_id"])
        self.registry_struc["ACC_NUM"] = self.acc_num_separator(kwargs["acc_number"])
        self.registry_struc["PASSWORD"] = kwargs["password"]
        self.registry_struc["NAME"] = kwargs["name"]
        self.registry_struc["L_NAME"] = kwargs["surname"]
        self.registry_struc["E_MAIL"] = kwargs["email"]
        self.registry_struc["PESEL"] = kwargs["pesel"]

        try:
            with open(self.registry_path, "r+") as f:
                self.registry_file["users"].append(self.registry_struc)
                f.write(json.dumps(self.registry_file))
            return {"STATUS": True, "ERROR": None, "DATA": self.registry_struc["ID"]}
        except Exception as e:
            return {"STATUS": False, "ERROR": "Unabe to register user!", "DATA": e}
