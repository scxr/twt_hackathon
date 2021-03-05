from pydantic import BaseModel, BaseSettings, BaseConfig
import os
class settings(BaseConfig):
    AUTH_SECRET = 'jwt_token'
    auth_jwt_secret_key = 'thisisasecrettest1234'
    DATABASE_URI = 'sqlite:///main.db'

class jwt_settings(BaseModel):
    auth_jwt_secret_key = os.urandom(16)