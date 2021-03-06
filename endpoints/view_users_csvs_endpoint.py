from fastapi import APIRouter, Depends, Request
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
    try:
        users_csvs = [csv["file"] for csv in csv_json[user]]
    except Exception as e:
        print(e)
        users_csvs = []
    
    return templates.TemplateResponse("view_csvs.html", {"request":request, "csvs":users_csvs})