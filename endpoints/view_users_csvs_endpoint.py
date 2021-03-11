from fastapi import APIRouter, Depends, Request
from .jwt_auth import decode_auth_token
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from db.functions import get_db
from models.database_models import User
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/my_csvs')
async def view_my_csvs(request: Request, Authorise: AuthJWT = Depends(), db = Depends(get_db)):
    Authorise.jwt_required()
    user = Authorise.get_jwt_subject()
    json_path = os.getcwd() + '\\db\\user_uploads.json'
    with open(json_path, 'r') as f:
        csv_json = json.load(f)
        f.close()
    
    users_csvs = [csv for csv in csv_json[user]]
    
            
    users_csvs = [csv for csv in csv_json[user]]

    #print([csv for csv in csv_json[user]])   
    print(users_csvs)
    return templates.TemplateResponse("view_csvs.html", {"request":request, "csvs":users_csvs, "user":f"Logged in as: {user}"})

@router.post('/delete_csv/{csv_id}')
async def delete_csv(csv_id:int, request: Request):
    user_cookie = request.cookies.get("access_token_cookie")
    if user_cookie == None:
        return RedirectResponse('/login')
    else:
        user_logged_in = decode_auth_token(user_cookie)
    print()
    file_path = os.getcwd()+ '\\upload_files\\' + str(csv_id)+'.csv'
    print(file_path, os.getcwd(), csv_id)
    os.remove(file_path)
    json_path = os.getcwd() + '\\db\\user_uploads.json'
    with open(json_path) as f:
        users_json = json.load(f)
    #users_json = json.load(json_path)
    for val in range(len(users_json[user_logged_in])):
        if users_json[user_logged_in][val]["file_id"] == csv_id:
            del users_json[user_logged_in][val]
            break
    with open(json_path, 'w') as f:
        json.dump(users_json, f)
    #json.dump()
    return 'done'
