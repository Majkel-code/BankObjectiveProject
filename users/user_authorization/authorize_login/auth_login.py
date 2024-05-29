from users.user_authorization.user_reader import UsersReader


class LoginAuthorization(UsersReader):
    def __init__(self) -> None:
        super().__init__()

    def check_login_data(self, login_id, password):
        """
        Checks the login data provided by the user against the registry file to determine if the
        login is successful.

        Args:
            login_id (str): The login ID of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary with the following keys:

                - "STATUS" (bool): Indicates whether the login is successful.
                - "ERROR" (str or None): If the login is not successful, this key contains an error message. Otherwise, it is None.
                - "DATA" (dict or None): If the login is successful, this key contains the user record. Otherwise, it is None.
        """
        for record in self.registry_file["users"]:
            if record["ID"] == login_id and record["PASSWORD"] == password:
                return {"STATUS": True, "ERROR": None, "DATA": record}
        return {"STATUS": False, "ERROR": "INCORRECT DATA"}
