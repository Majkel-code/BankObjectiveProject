import json
import os
from users.user_authorization.user_reader import UsersReader

class LoginAuthorization(UsersReader):
    def __init__(self) -> None:
        super().__init__()

    def check_login_data(self, login_id, password):
        for record in self.registry_file["users"]:
            print(record["ID"] == login_id)
            print(record["PASSWORD"] == password)
            if record["ID"] == login_id and record["PASSWORD"] == password:
                print("You can login!")
                return {"STATUS": True, "ERROR": None, "DATA": record}
        return {"STATUS": False, "ERROR": "INCORRECT DATA"}
            
    
