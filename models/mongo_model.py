from bson import ObjectId
from pydantic import BaseModel, BaseConfig


class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }
