from fastapi import APIRouter, Request, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from csv_functions.csv_functions_pandas import * 
from collections import defaultdict
import json
import os
import pandas as pd
router = APIRouter()
templates = Jinja2Templates(directory='templates')
@router.get('/view_csv')
async def reroute_select_csv(request: Request):
    try:
        tmp_cookie = request.cookies['access_token_cookie']
        return RedirectResponse('/my_csvs')
    except:
        return RedirectResponse('/login')

@router.get('/view_csv/{csv_id}')
async def view_csv(csv_id:int,request:Request,args='', columns='',Authorise : AuthJWT = Depends()):
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
    csv_cols = df.columns
    #val = await pandas_get_column_mean(df, "Industry_name_NZSIOC")
    csv_info = await pandas_np_general_information(df)
    vals = defaultdict(dict)
    for column in df.columns:
        column_mean = await pandas_get_column_mean(df, column)
        column_median = await pandas_get_column_median(df, column)
        column_mode = await pandas_get_column_mode(df, column)
        if str(column_mean) != "nan":
            vals[column]["mean"] = "%.2f" % column_mean
            vals[column]["median"] = "%.2f" % column_median
            vals[column]["mode"] = column_mode[0]
    print(dict(vals))
    print(dict(vals)["Year"]["mean"])
    for i in vals:
        print(vals[i]["mean"])
    return templates.TemplateResponse('csv_main.html', {"request":request, "csv_cols":csv_cols, "general":csv_info, "vals":dict(vals)})