from fastapi import APIRouter, Response, Form, Depends, Request
from fastapi.templating import Jinja2Templates
from .jwt_auth import encode_auth_token, jwt_required_wrap
from db.functions import get_db
from models.database_models import User
from fastapi_jwt_auth import AuthJWT

import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory='templates')
@router.post('/login')
async def login(response: Response, username=Form(...), password=Form(...), db = Depends(get_db), Authorise: AuthJWT = Depends()):
    user_vals = db.query(User).filter(User.username == username).first()
    print(user_vals)
    if user_vals is None:
        return {"error":"username not found"}
    if bcrypt.checkpw(password.encode(), user_vals.hashed_pword):
        access_token = Authorise.create_access_token(subject=username)
        Authorise.set_access_cookies(access_token)
        return {"access_token":access_token}
    else:
        return 'Incorrect password'

@router.get('/login')
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', {"request":request})