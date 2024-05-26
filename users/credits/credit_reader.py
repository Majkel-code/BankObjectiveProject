import json
import os

from users.credits.credit_construkt import CreditConstruct


class CreditReader(CreditConstruct):
    def __init__(self) -> None:
        super().__init__()

    def return_credit_data(self, id):
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
