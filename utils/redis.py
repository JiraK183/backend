import json
from typing import List, Any

import redis

from models import MongoModel
from utils.env import (
    get_env,
    REDIS_HOSTNAME,
    REDIS_PASSWORD,
    REDIS_PORT,
)


try:
    redis_client = redis.Redis(
        host=get_env(REDIS_HOSTNAME),
        password=get_env(REDIS_PASSWORD),
        port=get_env(REDIS_PORT),
    )
except Exception as e:
    raise Exception(
        "Redis failed to connect, environment variables could be missing.", e
    )


class AdvancedHashValue(MongoModel):
    redisValue: Any


def get_from_cache(key: str):
    cached_value = redis_client.get(key)

    if cached_value is None:
        return None

    json_value = json.loads(cached_value)

    if "redisValue" in json_value:
        return AdvancedHashValue(**json_value).redisValue

    return json_value


def cache(key: str, value, ex=None):
    if isinstance(value, List) or isinstance(value, dict):
        value = AdvancedHashValue(redisValue=value).json()

    redis_client.set(key, value, ex=ex)
