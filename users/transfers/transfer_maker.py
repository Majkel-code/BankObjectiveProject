import json
import os
from pathlib import Path
from users.user_authorization.user_reader import UsersReader


class TransferMaker:
    def __init__(self) -> None:
        self.path = Path(__file__).absolute().parents[1]
        self.transfers_path = f"{self.path}/transfers/transfer_data/transfers"
        self.transfers_file = {f"transfers": []}
        self.to_save = {f"transfers": []}
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

    def setup_files(self, user):
        if os.path.exists(f"{self.transfers_path}/{user}.json"):
            with open(f"{self.transfers_path}/{user}.json", "r") as f:
                self.transfers_file = json.load(f)
            return True
        return False

    def create_file(self, user):
        with open(f"{self.transfers_path}/{user}.json", "a") as f:
            f.write(json.dumps(self.transfers_file))

    def find_accounts(self):
        return UsersReader().find_account(
            to_acc_num=self.transfer_struc["TO_ACC"],
            from_acc_num=self.transfer_struc["FROM_ACC"],
            amount=self.transfer_struc["AMOUNT"])
    

    def find_user_id(self, acc_num):
        return UsersReader().find_id(acc_num=acc_num)

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


    def save_outcome(self, user, amount):
        user_id = self.find_user_id(user)
        print("IN SAVE OUTPUT!!!")
        self.transfer_struc["AMOUNT"] = -amount
        self.to_save["transfers"].append(self.transfer_struc)
        if self.setup_files(user=user_id["DATA"]):
            try:
                with open(f"{self.transfers_path}/{user_id['DATA']}.json", "r+") as f:
                    self.transfers_file["transfers"].append(self.transfer_struc)
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None}
            except:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!"}
        else:
            with open(f"{self.transfers_path}/{user_id['DATA']}.json", "a") as f:
                f.write(json.dumps(self.to_save))


    def save_income(self, user):
        if self.setup_files(user):
            try:
                with open(f"{self.transfers_path}/{user}.json", "r+") as f:
                    self.transfers_file["transfers"].append(self.transfer_struc)
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None}
            except:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!"}
        else:
            self.transfers_file["transfers"].append(self.transfer_struc)
            self.create_file(user=user)

    def save_transfer(self, **kwargs):
        self.transfer_struc["FROM_ACC"] = str(kwargs["from_acc"])
        self.transfer_struc["NAME"] = kwargs["name"]
        self.transfer_struc["L_NAME"] = kwargs["surname"]
        self.transfer_struc["TO_ACC"] = kwargs["to_acc"]
        self.transfer_struc["AMOUNT"] = kwargs["amount"]
        self.transfer_struc["DATE"] = kwargs["date"]
        self.transfer_struc["TITLE"] = kwargs["title"]
        self.transfer_struc["DESC"] = kwargs["desc"]

        
        finded_user = self.find_accounts()
        try:
            print("BEFORE ALL SAVEs")
            print(self.transfers_file)
            print(self.to_save)
            if finded_user["STATUS"]:
                self.save_income(user=finded_user['DATA'])
                print("after income SAVE")
                print(self.transfers_file)
                print(self.to_save)
            else:
                self.other_bank_user()
            self.save_outcome(user=self.transfer_struc["FROM_ACC"], amount=kwargs["amount"])
            return {"STATUS": True, "ERROR": None}
        except:
            return {"STATUS": False, "ERROR": "Unabe to register transfer!"}
        
