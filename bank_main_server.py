from pathlib import Path

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers.credit_form.take_credit as take_credit
import routers.load_transfer.load_transfers as load_transfers
import routers.login.login_req as login_req
import routers.register.register_req as register_req
from users.user_authorization.user_reader import UsersReader


class Server:
    def __init__(self) -> None:
        self.origins = ["*"]
        self.app = FastAPI()
        self.app.include_router(login_req.router)
        self.app.include_router(register_req.router)
        self.app.include_router(load_transfers.router)
        self.app.include_router(take_credit.router)
        self.server = uvicorn.Server
        UsersReader()
        current_path = Path(__file__).absolute().parent
        config_path = f"{current_path}/configs/config_files"
        with open(
            f"{config_path}/server_config.yaml",
            "r+",
        ) as f:
            server_config = yaml.safe_load(f)
        self.config = uvicorn.Config(
            app=self.app,
            port=server_config["PORT"],
            # log_config=None,
            log_level=server_config["LOG_LEVEL_SERVER"],
            host=server_config["HOST_IP"],
            reload=server_config["RELOAD"],
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._is_alive_ = False

    def start(self):
        if not self._is_alive_:
            try:
                self._is_alive_ = True
                self.server = self.server(self.config)
                self.server.run()
                print("SERVER CLOSED SUCCESSFUL!")
                self._is_alive_ = False
            except Exception as e:
                print(f"UNABLE TO ESTABLISH SERVER! {e}")


if __name__ == "__main__":
    start = Server()
    start.start()
