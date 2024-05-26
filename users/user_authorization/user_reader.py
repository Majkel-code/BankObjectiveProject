import json
import os
from pathlib import Path


class UsersReader:
    def __init__(self) -> None:
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
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r") as f:
                self.registry_file = json.load(f)
        else:
            self.create_file()

    def find_id(self, acc_num):
        for user in self.registry_file["users"]:
            if acc_num == user["ACC_NUM"]:
                return {"STATUS": True, "ERROR": None, "DATA": user["ID"]}
        return {"STATUS": False, "ERROR": "Unabe to find user data!", "DATA": None}

    def take_user_data(self, id):
        for user in self.registry_file["users"]:
            if user["ID"] == id:
                return {"STATUS": True, "ERROR": None, "DATA": user}
        return {"STATUS": False, "ERROR": "Unabe to find user data!", "DATA": None}

    def return_user_amount(self, id):
        for user in self.registry_file["users"]:
            if id == user["ID"]:
                return {"STATUS": True, "ERROR": None, "DATA": user["ACC_BALANSE"]}
        return {"STATUS": False, "ERROR": "Unabe to find user data!", "DATA": None}

    def calculate_incoming_balance(self, record, send_money):
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
        with open(self.registry_path, "a") as f:
            f.write(json.dumps(self.def_user))

    def acc_num_separator(self, number):
        return " ".join([number[i : i + 4] for i in range(0, len(number), 4)])

    def save_user_data(self, **kwargs):
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
