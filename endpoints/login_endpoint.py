from fastapi import APIRouter, Response, Form, Depends, Request, status
from fastapi.templating import Jinja2Templates
from db.functions import get_db
from models.database_models import User
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import RedirectResponse
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory='templates')
@router.post('/login')
async def login(response: Response, request:Request,username=Form(...), password=Form(...), db = Depends(get_db), Authorise: AuthJWT = Depends()):
    user_vals = db.query(User).filter(User.username == username).first()
    print(user_vals)
    if user_vals is None:
        return templates.TemplateResponse('login.html', {"request":request, "error":"username not found"})
    if bcrypt.checkpw(password.encode(), user_vals.hashed_pword):
        access_token = Authorise.create_access_token(subject=username)
        Authorise.set_access_cookies(access_token)
        rr = RedirectResponse('/my_csvs',status_code=status.HTTP_303_SEE_OTHER)
        rr.set_cookie("access_token_cookie", access_token)
        return rr
    else:
        return templates.TemplateResponse('login.html', {"request":request, "error":"Incorrect password"})

@router.get('/login')
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', {"request":request})