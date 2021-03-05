from pydantic import BaseModel
class User_req(BaseModel):
    username: str
    password: str