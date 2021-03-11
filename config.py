from pydantic import BaseModel, BaseSettings, BaseConfig
import os
class settings(BaseConfig):
    AUTH_SECRET = os.urandom(16)
    auth_jwt_secret_key = os.environ.get('JWT_SECRET')
    DATABASE_URI = 'sqlite:///main.db'

class jwt_settings(BaseModel):
    auth_jwt_secret_key = os.urandom(16)