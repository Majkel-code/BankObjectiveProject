from users.user_authorization.user_reader import UsersReader


class RegistryAuthorization(UsersReader):
    def __init__(self) -> None:
        super().__init__()

    def check_user_exist(self, pesel):
        """
        Check if a user with the given PESEL exists in the registry.

        Parameters:
            pesel (str): The PESEL number of the user to check.

        Returns:
            dict: A dictionary containing the status and error message.

                - "STATUS" (bool): True if the user does not exist, False if the user exists.
                - "ERROR" (str): The error message if the user exists, None otherwise.
        """
        for record in self.registry_file["users"]:
            if record["PESEL"] == pesel:
                return {"STATUS": False, "ERROR": "Urzytkownik o takich danych juz istnieje!"}
        return {"STATUS": True, "ERROR": None}

    def register_user(self, **kwargs):
        return self.save_user_data(**kwargs)
