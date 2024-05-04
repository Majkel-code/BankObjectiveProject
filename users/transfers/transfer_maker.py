import json
import os
from pathlib import Path
from users.user_authorization.user_reader import UsersReader


class TransferMaker:
    def __init__(self) -> None:
        self.path = Path(__file__).absolute().parents[1]
        self.transfers_path = f"{self.path}/transfers/transfer_data/transfers"
        self.transfers_file = {f"transfers": []}
        self.transfer_struc = {
            "FROM_ACC": None,
            "NAME": None,
            "L_NAME": None,
            "TO_ACC": None,
            "AMOUNT": None,
            "DATE": None,
            "TITLE": None,
            "DESC": None,
        }

    def create_file(self, user):
        print(self.transfers_path)
        with open(f"{self.transfers_path}/{user['DATA']}.json", "a") as f:
            f.write(json.dumps(self.transfers_file))

    def find_account(self):
        return UsersReader().find_account(acc_num=self.transfer_struc["TO_ACC"])

    def other_bank_user(self):
        if os.path.exists(f"{self.transfers_path}/differentBank.json"):
            try:
                with open(f"{self.transfers_path}/differentBank.json", "r+") as f:
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None}
            except:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!"}
        else:
            with open(f"{self.transfers_path}/differentBank.json", "a") as f:
                f.write(json.dumps(self.transfers_file))

    def save_transfer(self, **kwargs):
        print(kwargs)
        self.transfer_struc["FROM_ACC"] = str(kwargs["from_acc"])
        self.transfer_struc["NAME"] = kwargs["name"]
        self.transfer_struc["L_NAME"] = kwargs["surname"]
        self.transfer_struc["TO_ACC"] = kwargs["to_acc"]
        self.transfer_struc["AMOUNT"] = kwargs["amount"]
        self.transfer_struc["DATE"] = kwargs["date"]
        self.transfer_struc["TITLE"] = kwargs["title"]
        self.transfer_struc["DESC"] = kwargs["desc"]
        self.transfers_file["transfers"].append(self.transfer_struc)

        finded_user = self.find_account()
        if finded_user["STATUS"]:
            if os.path.exists(f"{self.transfers_path}/{finded_user['DATA']}.json"):
                try:
                    with open(f"{self.transfers_path}/{finded_user['DATA']}.json", "r+") as f:
                        f.write(json.dumps(self.transfers_file))
                    return {"STATUS": True, "ERROR": None}
                except:
                    return {"STATUS": False, "ERROR": "Unabe to register transfer!"}
            else:
                self.create_file(user=finded_user)
        else:
            self.other_bank_user()
