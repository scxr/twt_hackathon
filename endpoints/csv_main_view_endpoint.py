from fastapi import APIRouter, Request, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import RedirectResponse
import json
import os
import pandas as pd
router = APIRouter()

@router.get('/view_csv')
async def reroute_select_csv(request: Request):
    try:
        tmp_cookie = request.cookies['access_token_cookie']
        return RedirectResponse('/my_csvs')
    except:
        return RedirectResponse('/login')

@router.get('/view_csv/{csv_id}')
async def view_csv(csv_id:int, Authorise : AuthJWT = Depends()):
    Authorise.jwt_required()
    user = Authorise.get_jwt_subject()
    path = os.getcwd() + '\\db\\user_uploads.json'
    with open(path) as f:
        users_json = json.load(f)
    users_csvs = users_json[user]
    csv_path = os.getcwd() + '\\upload_files\\' + str(csv_id) + '.csv'
    df = pd.read_csv(csv_path)
    columns = [i for i in df.columns]
    return columns