from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from db.base import SessionLocal, engine
from sqlalchemy.orm import Session
from db.functions import get_db
from models.database_models import User
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/register')
async def register_get(request:Request):
    return templates.TemplateResponse('register.html', {'request':request})

@router.post('/register')
async def register(request:Request, username=Form(...), password=Form(...), password_confirm=Form(...),db:Session = Depends(get_db)):
    print(isinstance(request, Request))
    if password != password_confirm:
        return templates.TemplateResponse('register.html', {'request':request, 'error':'Invalid Password'})
    hashed_pword = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()
    )
    user_sent = User()
    user_sent.hashed_pword = hashed_pword
    user_sent.username = username
    try:
        db.add(user_sent)
        db.commit()
    except Exception as e:
        return {"error":"user name already in use"}
    return {"ok":"user created"}