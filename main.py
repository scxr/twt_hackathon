from logging import debug
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
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
import os
from db.base import Base, engine
from config import jwt_settings
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

class Settings(BaseModel):
    authjwt_secret_key: str = os.environ.get('JWT_SECRET')
    authjwt_token_location: set = {"cookies"} 

@AuthJWT.load_config
def get_config():
    return Settings()

Base.metadata.create_all(engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/graphs", StaticFiles(directory="graphs"), name="graphs")

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request:Request, exc: AuthJWTException):
    return RedirectResponse('/login')
app.include_router(hello_world_endpoint.router)
app.include_router(upload_csv_endpoint.router)
app.include_router(login_endpoint.router)
app.include_router(register_endpoint.router)
app.include_router(view_users_csvs_endpoint.router)
app.include_router(index_endpoint.router)
app.include_router(logout_endpoint.router)
app.include_router(csv_main_view_endpoint.router)
#port = int(os.environ.get('PORT', 5000))
#uvicorn.run(app, host="0.0.0.0", port=port, debug=False)