from pydantic import BaseModel


class CurrentUser(BaseModel):
    space: str
    username: str
    api_key: str
