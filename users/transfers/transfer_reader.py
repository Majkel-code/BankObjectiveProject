import json
import os
from pathlib import Path

class TransferReader:
    def __init__(self) -> None:
        self.path = Path(__file__).absolute().parents[1]
        self.history_path = f"{self.path}/transfers/transfer_data/transfers/"
        self.registry_file = {f"history": []}



    def check_history(self, user_id):
        if os.path.exists(f"{self.history_path}{user_id}.json"):
            with open(f"{self.history_path}{user_id}.json", "r") as f:
                return {"STATUS": True, "ERROR": None, "DATA": json.load(f)}
        else:
            return {"STATUS": False, "ERROR": "There is no data to load!"}
        


