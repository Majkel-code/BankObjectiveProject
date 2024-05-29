from pathlib import Path

import yaml


class ConfigReturner:
    def __init__(self) -> None:
        self.current_path = Path(__file__).absolute().parent

    def credit_config_returner(self):
        """
        Reads the credit configuration from a YAML file and returns it as a dictionary.

        Returns:
            dict: A dictionary containing the credit configuration. The dictionary has the following keys:

                - "STATUS" (bool): Indicates whether the retrieval was successful.
                - "ERROR" (str or None): If the retrieval was not successful, this key contains an error message. Otherwise, it is None.
                - "DATA" (dict or None): If the retrieval was successful, this key contains the credit configuration. Otherwise, it is None.
        """
        with open(
            f"{self.current_path}/config_files/credits_config.yaml",
            "r+",
        ) as f:
            credit_config = yaml.safe_load(f)
            return {"STATUS": True, "ERROR": None, "DATA": credit_config}
