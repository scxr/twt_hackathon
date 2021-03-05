from pydantic import BaseModel, BaseSettings, BaseConfig

class settings(BaseConfig):
    AUTH_SECRET = 'jwt_token'
    DATABASE_URI = 'sqlite:///main.db'