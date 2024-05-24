from pathlib import Path

import yaml

class ConfigReturner:
    def __init__(self) -> None:
        self.current_path = Path(__file__).absolute().parent

    def credit_config_returner(self):
        with open(f"{self.current_path}/config_files/credits_config.yaml","r+",) as f:
                credit_config = yaml.safe_load(f)
                return {"STATUS": True, "ERROR": None, "DATA": credit_config}