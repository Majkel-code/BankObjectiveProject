from pathlib import Path
import yaml
import json
from users.transfers.transfer_maker import TransferMaker


class CreditConstruct:
    def __init__(self) -> None:
        self.path = Path(__file__).absolute().parents[2]
        self.credit_path = f"{self.path}/users/credits/credit_data"
        self.credit_file = {f"credits": []}
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
        with open(f"{self.path}/configs/config_files/credits_config.yaml", "r") as f:
            return yaml.safe_load(f)

    def create_credit_file(self, id):
        try:
            with open(f"{self.credit_path}/{id}.json", "a") as f:
                f.write(json.dumps(self.credit_file))
            return {"STATUS": True, "ERROR": None, "DATA": None}
        except Exception as e:
            return {"STATUS": False, "ERROR": "Unabe to save credit data!", "DATA": e}

    def edit_credit_file(self, id):
        try:
            with open(f"{self.credit_path}/{id}.json", "w") as f:
                json.dump(self.credit_file, f)
            return {"STATUS": True, "ERROR": None, "DATA": None}
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to save credit data!", "DATA": e}

    def add_credit_amount_to_account(self, id, data):
        print("GO TO SEND TRANSFER")
        return TransferMaker().credit_income_save(id, **data)

    def calculate_excess_credit(self, id, data):
        return TransferMaker().credit_outcome_save(id, **data)
