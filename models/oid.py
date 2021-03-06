from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, oid):
        try:
            return ObjectId(str(oid))
        except InvalidId:
            raise HTTPException(
                status_code=400, detail="Could not parse invalid ObjectId."
            )
