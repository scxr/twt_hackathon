from fastapi import APIRouter, Request, Depends, Form
from fastapi_jwt_auth import AuthJWT
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from csv_functions.csv_functions_pandas import * 
from collections import defaultdict
from csv_functions.graph_functions import parse_request
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
async def view_csv(csv_id:int,request:Request,colo='', colt='',graph_type='',Authorise : AuthJWT = Depends()):
    Authorise.jwt_required()
    user = Authorise.get_jwt_subject()
    user_to_send = f'Logged in as: {user}'
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
        #print(column)
        column_mean = await pandas_get_column_mean(df, column)
        column_median = await pandas_get_column_median(df, column)
        column_mode = await pandas_get_column_mode(df, column)

        if str(column_mean) != "nan":
            vals[column]["mean"] = "%.2f" % column_mean
            vals[column]["median"] = "%.2f" % column_median
            vals[column]["mode"] = column_mode[0]

    resp = await parse_request(df, graph_type, colo, colt, csv_id)
    images = []
    try:
        for i in os.listdir(f'graphs\\{csv_id}'):
            images.append(str(csv_id)+'\\'+i)
    except:
        images = []
    return templates.TemplateResponse('csv_main.html', {"request":request, 
                                                        "csv_cols":csv_cols, 
                                                        "general":csv_info, 
                                                        "vals":dict(vals),
                                                        "csv_id":csv_id,
                                                        "images":images,
                                                        "user":user_to_send})

@router.post('/add_graph/{csv_id}')
async def add_graph_post(csv_id:int, graphtype=Form(...), col1=Form(...), col2=Form(...)):
    return RedirectResponse(f'/view_csv/{csv_id}?colo={col1}&colt={col2}&graph_type={graphtype}', status_code=303)

@router.get('/add_graph/{csv_id}')
async def add_graph(request: Request, csv_id:int):
    csv_path = os.getcwd() + '\\upload_files\\' + str(csv_id) + '.csv'
    df = pd.read_csv(csv_path)
    plottable_columns = await pandas_get_possible_numerics(df)
    return templates.TemplateResponse('add_graph.html', {"request":request, "columns":plottable_columns})



@router.get('/remove_graph/{csv_id}/{fp}')
async def remove_graph(csv_id:int, fp:str):
    os.remove(f'graphs/{csv_id}/{fp}')
    print(fp, csv_id)
    return RedirectResponse(f'/view_csv/{csv_id}', status_code=303)