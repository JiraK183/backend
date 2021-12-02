from pymongo import MongoClient

from utils.env import (
    get_env,
    MONGO_DATABASE,
    MONGO_HOSTNAME,
    MONGO_PORT,
    MONGO_USERNAME,
    MONGO_PASSWORD,
)

try:
    mongo_client = MongoClient(
        host=get_env(MONGO_HOSTNAME),
        port=int(get_env(MONGO_PORT)),
        authSource="admin",
        username=get_env(MONGO_USERNAME),
        password=get_env(MONGO_PASSWORD),
    )[get_env(MONGO_DATABASE)]
except Exception as e:
    raise Exception(
        "MongoDB failed to connect, environment variables could be missing.", e
    )
