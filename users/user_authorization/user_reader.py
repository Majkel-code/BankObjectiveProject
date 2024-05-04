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
        print(self.users_path)
        self.setup_files()


    def setup_files(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r") as f:
                self.registry_file = json.load(f)
        else:
            self.create_file()


    def find_account(self, acc_num):
        self.setup_files()
        for record in self.registry_file["users"]:
            if record["ACC_NUM"] == acc_num:
                return {"STATUS": True, "ERROR": None, "DATA": record["ID"]}
        return {"STATUS": False, "ERROR": "There is no account", "DATA": None}


    def create_file(self):
        with open(self.registry_path, "a") as f:
                f.write(json.dumps(self.def_user))


    def acc_num_separator(self, number):
        return ' '.join([number[i:i+4] for i in range(0, len(number), 3)])

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
            return {"STATUS": True, "ERROR": None}
        except:
            return {"STATUS": False, "ERROR": "Unabe to register user!"}
 
