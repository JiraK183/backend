import os
from typing import Optional

from dotenv import load_dotenv

MONGO_HOSTNAME = "MONGO_HOSTNAME"
MONGO_PORT = "MONGO_PORT"
MONGO_USERNAME = "MONGO_USERNAME"
MONGO_PASSWORD = "MONGO_PASSWORD"
MONGO_DATABASE = "MONGO_DATABASE"
REDIS_HOSTNAME = "REDIS_HOSTNAME"
REDIS_PASSWORD = "REDIS_PASSWORD"
REDIS_PORT = "REDIS_PORT"

load_dotenv(".env")


def get_env(env_var: str) -> Optional[str]:
    return os.environ[env_var] if env_var in os.environ else None
