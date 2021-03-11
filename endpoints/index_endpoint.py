from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from endpoints.jwt_auth import decode_auth_token
router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get('/')
async def index(request: Request, Authorise: AuthJWT = Depends()):
    try:
        auth_cookie = request.cookies["access_token_cookie"]
        myuser = decode_auth_token(auth_cookie)
        if myuser is None:
            user = "Not logged in"
        else:
            user = f'Logged in as: {myuser}'
    except:
        user = "Not logged in"
    print(user)
    
    return templates.TemplateResponse('index.html', {"request":request, "user":user})
