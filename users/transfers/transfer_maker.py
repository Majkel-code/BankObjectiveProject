import json
import os
from pathlib import Path
from users.user_authorization.user_reader import UsersReader


class TransferMaker:
    def __init__(self) -> None:
        self.path = Path(__file__).absolute().parents[1]
        self.history_path = f"{self.path}/transfers/transfer_data/history"
        self.receiver_to_save = {"history": []}
        self.sender_to_save = {"history": []}
        self.transfers_path = f"{self.path}/transfers/transfer_data/transfers"
        self.transfers_file = {f"transfers": []}
        self.to_save = {f"transfers": []}
        self.transfer_struc = {
            "FROM_ACC": None,
            "SENDER": None,
            "TO_ACC": None,
            "RECEIVER": None,
            "AMOUNT": None,
            "DATE": None,
            "TIME": None,
            "TITLE": None,
            "DESC": None,
        }

    def setup_files(self, user):
        if os.path.exists(f"{self.transfers_path}/{user}.json"):
            with open(f"{self.transfers_path}/{user}.json", "r") as f:
                self.transfers_file = json.load(f)
            return {"STATUS": True, "ERROR": None}
        return {"STATUS": False, "ERROR": "Unable to setup file!"}

    def create_file(self, user):
        try:
            with open(f"{self.transfers_path}/{user}.json", "a") as f:
                f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None}
        except:
            return {"STATUS": False, "ERROR": "Unable to create file!"}

    def find_accounts(self, id: int = None):
        if id is not None:
            return UsersReader().find_account(
                to_acc_num=None,
                from_acc_num=None,
                amount=self.transfer_struc["AMOUNT"],
                id=id,)
        else:
            return UsersReader().find_account(
                to_acc_num=self.transfer_struc["TO_ACC"],
                from_acc_num=self.transfer_struc["FROM_ACC"],
                amount=self.transfer_struc["AMOUNT"])  

    def find_user_id(self, acc_num):
        return UsersReader().find_id(acc_num=acc_num)
    
    def income_path_user(self, finded_user_income):
        try:
            if os.path.exists(f"{self.transfers_path}/{finded_user_income['DATA']["ID"]}.json"):
                return True
        except:
            return False
        
    def outcome_path_user(self, finded_user_outcome):
        try:
            if os.path.exists(f"{self.transfers_path}/{finded_user_outcome["DATA"]}.json"):
                return True
        except:
            return False
    
    def setup_history_path(self, user, file):
        if os.path.exists(f"{self.history_path}/{user}.json"):
            with open(f"{self.history_path}/{user}.json", "r") as f:
                file = json.load(f)
            return file
        return False
    

    def save_to_history(self, id):
        receiver_to_save = {"history": []}
        sender_to_save = {"history": []}
        if id is not None:
            if self.setup_files(user=id)["STATUS"]:
                if len(self.transfers_file["transfers"]) >=3:
                    if os.path.exists(f"{self.history_path}/{id}.json"):
                        with open(f"{self.history_path}/{id}.json", "r") as f:
                            self.receiver_to_save = json.load(f)
                    else:
                        with open(f"{self.history_path}/{id}.json", "a") as f:
                            f.write(json.dumps(self.receiver_to_save))
                    self.receiver_to_save["history"].append(self.transfers_file["transfers"][0])
                    del self.transfers_file["transfers"][0]


                    with open(f"{self.transfers_path}/{id}.json", "w") as f:
                        json.dump(self.transfers_file, f)


                    with open(f"{self.history_path}/{id}.json", "r+") as f:
                        f.write(json.dumps(self.receiver_to_save))   

        # if sender is not None:
        #     if self.setup_files(user=sender)["STATUS"]:
        #         if len(self.transfers_file["transfers"]) >=3:
        #             if os.path.exists(f"{self.history_path}/{sender}.json"):
        #                 with open(f"{self.history_path}/{sender}.json", "r") as f:
        #                     self.sender_to_save = json.load(f)
        #             else:
        #                 with open(f"{self.history_path}/{sender}.json", "a") as f:
        #                     f.write(json.dumps(self.sender_to_save))
        #             self.sender_to_save["history"].append(self.transfers_file["transfers"][0])
        #             del self.transfers_file["transfers"][0]


        #             with open(f"{self.transfers_path}/{sender}.json", "w") as f:
        #                 json.dump(self.transfers_file, f)


        #             with open(f"{self.history_path}/{sender}.json", "r+") as f:
        #                 f.write(json.dumps(self.sender_to_save))   
                             
                
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


    def save_outcome(self, user_sender, amount):      
        user_id = user_sender
        self.transfer_struc["AMOUNT"] = -amount
        self.to_save["transfers"].append(self.transfer_struc)
        if self.setup_files(user=user_id)["STATUS"]:
            try:
                with open(f"{self.transfers_path}/{user_id}.json", "r+") as f:
                    self.transfers_file["transfers"].append(self.transfer_struc)
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None}
            except:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!"}
        else:
            with open(f"{self.transfers_path}/{user_id}.json", "a") as f:
                f.write(json.dumps(self.to_save))


    def save_income(self, user):
        if self.setup_files(user)["STATUS"]:
            try:
                with open(f"{self.transfers_path}/{user}.json", "r+") as f:
                    self.transfers_file["transfers"].append(self.transfer_struc)
                    f.write(json.dumps(self.transfers_file))
                return {"STATUS": True, "ERROR": None}
            except:
                return {"STATUS": False, "ERROR": "Unabe to register transfer!"}
        else:
            self.transfers_file["transfers"].append(self.transfer_struc)
            return self.create_file(user=user)


    def credit_income_save(self, id: int, **kwargs):
        print(kwargs)
        self.transfer_struc = kwargs
        print("HERE")
        print(self.transfer_struc)
        finded_user_income = self.find_accounts(id)
        print("FINDED_USER_INCOME")
        print(finded_user_income)
        if self.income_path_user(id):
            self.save_to_history(
                id=id,
                )
        try:
            self.save_income(user=finded_user_income['DATA']["ID"])
            return UsersReader().return_user_amount(id=id)
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to register credit transfer!", "DATA": e}

    def perform_outcome(self, id, send_money):
        UsersReader().calculate_outcoming_balance(acc_num=None, send_money=send_money, id=id)

    def credit_outcome_save(self, id: int, **kwargs):
        print("IN CREDIT OUTCOME SAVE")
        print(kwargs)
        self.transfer_struc["SENDER"] = kwargs["sender"]
        self.transfer_struc["RECEIVER"] = "CoronaBank S.A."
        self.transfer_struc["FROM_ACC"] = str(kwargs["from_acc"])
        self.transfer_struc["TO_ACC"] = kwargs["to_acc"]
        self.transfer_struc["AMOUNT"] = kwargs["amount"]
        self.transfer_struc["DATE"] = kwargs["date"]
        self.transfer_struc["TIME"] = kwargs["time"]
        self.transfer_struc["TITLE"] = kwargs["title"]
        self.transfer_struc["DESC"] = kwargs["desc"]
        amount = kwargs["amount"]
        self.transfer_struc["AMOUNT"] = -amount
        print("HERE outcome")
        print(self.transfer_struc)

        if self.income_path_user(id):
            self.save_to_history(
                id=id,
                )
        try:
            self.save_outcome(user_sender=id, amount=kwargs["amount"])
            self.perform_outcome(id=id, send_money=kwargs["amount"])
            return UsersReader().return_user_amount(id=id)
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to register credit transfer!", "DATA": e}
        

    def save_transfer(self, **kwargs):
        if kwargs["company"] != '':
            self.transfer_struc["RECEIVER"] = kwargs["company"]
        self.transfer_struc["SENDER"] = kwargs["sender"]
        self.transfer_struc["FROM_ACC"] = str(kwargs["from_acc"])
        self.transfer_struc["TO_ACC"] = kwargs["to_acc"]
        self.transfer_struc["AMOUNT"] = kwargs["amount"]
        self.transfer_struc["DATE"] = kwargs["date"]
        self.transfer_struc["TIME"] = kwargs["time"]
        self.transfer_struc["TITLE"] = kwargs["title"]
        self.transfer_struc["DESC"] = kwargs["desc"]

        finded_user_income = self.find_accounts()
        finded_user_outcome = self.find_user_id(self.transfer_struc["FROM_ACC"])
        print(finded_user_income)
        print(finded_user_outcome)

        if self.income_path_user(finded_user_income):
            self.save_to_history(
                id=finded_user_income['DATA']["ID"],
                )        
        if self.outcome_path_user(finded_user_outcome):
            self.save_to_history(
                id=finded_user_outcome['DATA'],
                )   
        try:
            if finded_user_income["STATUS"]:
                self.transfer_struc["RECEIVER"] = finded_user_income['DATA']["RECEIVER"]
                self.save_income(user=finded_user_income['DATA']["ID"])
            else:
                self.transfers_file["transfers"].append(self.transfer_struc)
                self.other_bank_user()
            self.save_outcome(user_sender=finded_user_outcome["DATA"], amount=kwargs["amount"])
            return UsersReader().return_user_amount(finded_user_outcome['DATA'])
        except Exception as e:
            print(e)
            return {"STATUS": False, "ERROR": "Unabe to register transfer!", "DATA": e}
        
        
