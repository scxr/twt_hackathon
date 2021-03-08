from fastapi import APIRouter, Request, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import RedirectResponse
from csv_functions.csv_functions_pandas import * 
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
async def view_csv(csv_id:int,args='', columns='',Authorise : AuthJWT = Depends()):
    Authorise.jwt_required()
    to_zip = False
    if ',' in args:
        to_zip = True
        args = args.split(',')
    if ',' in columns:
        to_zip = True
        columns = columns.split(',')
    
    print(args, columns)
    if to_zip:
        args_and_cols = zip(args, columns)
    else:
        args_and_cols = zip([args], [columns])
    user = Authorise.get_jwt_subject()
    path = os.getcwd() + '\\db\\user_uploads.json'
    with open(path) as f:
        users_json = json.load(f)
    users_csvs = users_json[user]
    csv_path = os.getcwd() + '\\upload_files\\' + str(csv_id) + '.csv'
    df = pd.read_csv(csv_path)
    val = await pandas_get_column_mean(df, "Industry_name_NZSIOC")
    return str(val)