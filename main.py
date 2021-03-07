from fastapi import FastAPI, Request
from endpoints import (hello_world_endpoint,
                       upload_csv_endpoint,
                       login_endpoint,
                       register_endpoint,
                       view_users_csvs_endpoint,
                       index_endpoint,
                       logout_endpoint,
                       csv_main_view_endpoint)
from pydantic import BaseModel                       
import uvicorn
from db.base import Base, engine
from config import jwt_settings
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

class Settings(BaseModel):
    authjwt_secret_key: str = "thisisasecrettest1234"
    authjwt_token_location: set = {"cookies"} 

@AuthJWT.load_config
def get_config():
    return Settings()

Base.metadata.create_all(engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request:Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail":exc.message}
    )
app.include_router(hello_world_endpoint.router)
app.include_router(upload_csv_endpoint.router)
app.include_router(login_endpoint.router)
app.include_router(register_endpoint.router)
app.include_router(view_users_csvs_endpoint.router)
app.include_router(index_endpoint.router)
app.include_router(logout_endpoint.router)
app.include_router(csv_main_view_endpoint.router)
uvicorn.run(app)