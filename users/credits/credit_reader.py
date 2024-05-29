import json
import os

from users.credits.credit_construkt import CreditConstruct


class CreditReader(CreditConstruct):
    def __init__(self) -> None:
        """Initializes a new instance of the class.

        This constructor sets up the necessary attributes for the class.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()

    def return_credit_data(self, id):
        """Returns the credit data for a given user ID.

        Args:
            id (int): The ID of the user.

        Returns:
            dict: A dictionary containing the credit data. The dictionary has the following structure:

                    * "STATUS" (bool): Indicates whether the credit data was successfully retrieved.
                    * "ERROR" (str or None): If "STATUS" is False, this field contains an error message. Otherwise, it is None.
                    * "DATA" (dict or None): If "STATUS" is True, this field contains the credit data. Otherwise, it is None.
        """
        if os.path.exists(f"{self.credit_path}/{id}.json"):
            credit_data: dict
            try:
                with open(f"{self.credit_path}/{id}.json", "r") as f:
                    credit_data = json.load(f)
            except Exception as e:
                return {"STATUS": False, "ERROR": "Unable to load user credit!", "DATA": e}
            return {"STATUS": True, "ERROR": None, "DATA": credit_data}
        else:
            return {"STATUS": False, "ERROR": "You don't have active credit!", "DATA": None}
