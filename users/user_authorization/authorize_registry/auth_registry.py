from users.user_authorization.user_reader import UsersReader


class RegistryAuthorization(UsersReader):
    def __init__(self) -> None:
        super().__init__()

    def check_user_exist(self, pesel):
        for record in self.registry_file["users"]:
            if record["PESEL"] == pesel:
                return {"STATUS": False, "ERROR": "Urzytkownik o takich danych juz istnieje!"}
        return {"STATUS": True, "ERROR": None}

    def register_user(self, **kwargs):
        return self.save_user_data(**kwargs)
