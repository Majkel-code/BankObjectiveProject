import json
import os
from pathlib import Path

class TransferReader:
    def __init__(self) -> None:
        self.path = Path(__file__).absolute().parents[1]
        self.history_path = f"{self.path}/transfers/transfer_data/"
        self.registry_file = {f"history": []}



    def take_dict_key(self, dict):
        return [*dict]


    def check_history(self, user_id):
        if os.path.exists(f"{self.history_path}transfers/{user_id}.json"):
            with open(f"{self.history_path}transfers/{user_id}.json", "r") as f:
                data = json.load(f)
                if len(data["transfers"]) > 3:
                    data_to_return = {f"{self.take_dict_key(data)[0]}": data["transfers"][-3:][::-1]}
                    return {"STATUS": True, "ERROR": None, "DATA": data_to_return}
                
                data_to_return = {f"{self.take_dict_key(data)[0]}": data["transfers"][::-1]}
                return {"STATUS": True, "ERROR": None, "DATA": data_to_return}
        else:
            return {"STATUS": False, "ERROR": "There is no data to load!", "DATA": None}
        

    def take_def_transactions(self):
        if os.path.exists(f"{self.history_path}history/def_transactions.json"):
            with open(f"{self.history_path}history/def_transactions.json", "r") as f:
                return {"STATUS": True, "ERROR": None, "DATA": json.load(f)}
        


