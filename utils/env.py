import os
from typing import Optional

from dotenv import load_dotenv

API_PORT = "API_PORT"

MONGO_HOSTNAME = "MONGO_HOSTNAME"
MONGO_PORT = "MONGO_PORT"
MONGO_USERNAME = "MONGO_USERNAME"
MONGO_PASSWORD = "MONGO_PASSWORD"
MONGO_DATABASE = "MONGO_DATABASE"

JIRA_SPACE = "JIRA_SPACE"
JIRA_USERNAME = "JIRA_USERNAME"
JIRA_API_KEY = "JIRA_API_KEY"

load_dotenv(".env")


def get_env(env_var: str) -> Optional[str]:
    return os.environ[env_var] if env_var in os.environ else None
