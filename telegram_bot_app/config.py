import json
import os


def get_bot_token():
    with open("secrets/token.json", "r") as fh:
        return json.load(fh)


hostname = os.environ.get("API_HOST") or "localhost"
host_port = os.environ.get("API_PORT") or "5000"


class Config:
    bot = get_bot_token()
    bot_name = bot["bot"]
    bot_token = bot["token"]
    users_api_url = f"http://{hostname}:{host_port}/api/v1/users"
    new_user_api_url = f"http://{hostname}:{host_port}/api/v1/users"
