from fastapi import File, UploadFile, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from .jwt_auth import encode_auth_token, jwt_required_wrap, decode_auth_token
from fastapi_jwt_auth import AuthJWT
import json
import os
import random
from datetime import datetime as dt
import magic
router = APIRouter()
m = magic.Magic(mime=True)
templates = Jinja2Templates(directory='templates')
class csv:
    def __init__(self, csv_name, date_uploaded, user_upload_by):
        self.csv_name =csv_name
        self.date_uploaded = date_uploaded
        self.user_upload_by = user_upload_by
@router.post('/upload_csv')
async def create_upload_file(request: Request, file : UploadFile = File(...)):
    file_id = random.randint(111111,999999)
    auth_cookie = request.cookies["access_token_cookie"]
    user = decode_auth_token(auth_cookie)
    
    if file.filename.endswith('.csv'):
        path = os.getcwd() + '\\upload_files\\' + str(file_id) + '.csv'
    else:
        return {"error":"file extension must be .csv"}
    with open(path, 'wb+') as f:
        f.write(file.file.read())
        f.close()
    
    file_type = m.from_file(path)
    if file_type != 'text/plain':
        return {"error":"This is not a valid csv file."}

    json_path = os.getcwd() + '\\db\\user_uploads.json'
    
    with open(json_path, 'r') as f:
        current_data = json.loads(f.read())
        f.close()
    print(type(file.filename))
    try:
        users_data = current_data[user]
        current_data[user].append({"file":file.filename,"date":str(dt.utcnow()), "file_id":file_id})
    except Exception as e:
        print(e)
        current_data[user] = []
        current_data[user].append({"file":file.filename, "date":str(dt.utcnow()), "file_id":file_id})
    
    with open(json_path, 'w') as fp:
        print(type(current_data))
        json.dump(current_data, fp)
    return RedirectResponse('/my_csvs', status_code=303)


@router.get('/upload_csv')
async def get_upload_file(request: Request, Authorise: AuthJWT = Depends()):
    Authorise.jwt_required()
    user = Authorise.get_jwt_subject()
    return templates.TemplateResponse("upload_csv.html", {"request":request, "user":user})