import json
import os
from pathlib import Path


class TransferReader:
    def __init__(self) -> None:
        """
        Initializes a new instance of the TransferReader class.

        This constructor sets up the necessary attributes for the TransferReader class. It initializes the following attributes:

            - `path`: The absolute path to the parent directory of the current file, level up one.
            - `history_path`: The path to the transfer history data directory, which is located in the `transfers/transfer_data` directory of the parent directory of the current file.
            - `registry_file`: An empty dictionary representing the transfer history registry file.

        Args:
            None

        Returns:
            None
        """
        self.path = Path(__file__).absolute().parents[1]
        self.history_path = f"{self.path}/transfers/transfer_data/"
        self.registry_file = {"history": []}

    def take_dict_key(self, dict):
        """
        Takes a dictionary and returns a list of its keys.

        Parameters:
            dict (dict): The dictionary to extract keys from.

        Returns:
            list: A list containing the keys of the dictionary.
        """
        return [*dict]

    def check_history(self, user_id):
        """
        Check the history of a user's transfers.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: A dictionary containing the following keys:

                    - "STATUS" (bool): Indicates whether the operation was successful.
                    - "ERROR" (str or None): If the operation was not successful, this key contains an error message. Otherwise, it is None.
                    - "DATA" (dict or None): The loaded default transactions data.
        If the operation was successful and there are more than 3 transfers,
        the data is a dictionary with the following keys:
                - The first key of the input dictionary (obtained using `self.take_dict_key(data)[0]`)
                - The last 3 transfers in reverse order (obtained using `data["transfers"][-3:][::-1]`)
        - If the operation was successful and there are less than or equal to 3 transfers,
        the data is a dictionary with the following keys:
                - The first key of the input dictionary (obtained using `self.take_dict_key(data)[0]`)
                - All the transfers in reverse order (obtained using `data["transfers"][::-1]`)
        - If the operation was not successful, the data is None.
        """
        if os.path.exists(f"{self.history_path}transfers/{user_id}.json"):
            with open(f"{self.history_path}transfers/{user_id}.json", "r") as f:
                data = json.load(f)
                if len(data["transfers"]) > 3:
                    data_to_return = {
                        f"{self.take_dict_key(data)[0]}": data["transfers"][-3:][::-1]
                    }
                    return {"STATUS": True, "ERROR": None, "DATA": data_to_return}

                data_to_return = {f"{self.take_dict_key(data)[0]}": data["transfers"][::-1]}
                return {"STATUS": True, "ERROR": None, "DATA": data_to_return}
        else:
            return {"STATUS": False, "ERROR": "There is no data to load!", "DATA": None}

    def take_def_transactions(self):
        """
        Retrieves the default transactions from the history file.

        This function checks if the default transactions file exists in the specified history path.
        If the file exists, it opens the file and reads its contents using the `json.load()` function.
        The contents are then returned as a dictionary with the following keys:

                - "STATUS": A boolean indicating whether the operation was successful.
                - "ERROR": A string or None indicating any error that occurred during the operation. If the operation was successful, this key is set to None.
                - "DATA": The loaded default transactions data.

        Returns:
            dict: A dictionary containing the following keys:

                    - "STATUS" (bool):
                        - Indicates whether the operation was successful.
                    - "ERROR" (str or None):
                        - If the operation was not successful, this key contains an error message. Otherwise, it is None.
                    - "DATA" (dict):
                        - The loaded default transactions data.

        Raises:
            FileNotFoundError: If the default transactions file does not exist in the specified history path.
        """
        if os.path.exists(f"{self.history_path}history/def_transactions.json"):
            with open(f"{self.history_path}history/def_transactions.json", "r") as f:
                return {"STATUS": True, "ERROR": None, "DATA": json.load(f)}
