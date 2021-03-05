from fastapi import File, UploadFile, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from .jwt_auth import encode_auth_token, jwt_required_wrap, decode_auth_token
from fastapi_jwt_auth import AuthJWT
import json
import os
router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.post('/upload_file')
async def create_upload_file(request: Request, file : UploadFile = File(...)):
    auth_cookie = request.cookies["access_token_cookie"]
    user = decode_auth_token(auth_cookie)
    
    if file.filename.endswith('.csv'):
        path = os.getcwd() + '\\upload_files\\' + file.filename
    else:
        return {"error":"file extension must be .csv"}
    with open(path, 'wb+') as f:
        f.write(file.file.read())
        f.close()
    json_path = os.getcwd() + '\\db\\user_uploads.json'
    
    with open(json_path, 'r') as f:
        current_data = json.loads(f.read())
        f.close()
    print(type(file.filename))
    try:
        users_data = current_data[user]
        current_data[user].append({"file":file.filename})
    except Exception as e:
        print(e)
        current_data[user] = []
        current_data[user].append({"file":file.filename})
    
    with open(json_path, 'w') as fp:
        print(type(current_data))
        json.dump(current_data, fp)
    return {"filename":str(file.filename)}

@router.get('/upload_file')
async def get_upload_file(request: Request, Authorise: AuthJWT = Depends()):
    Authorise.jwt_required()
    user = Authorise.get_jwt_subject()
    return templates.TemplateResponse("upload_csv.html", {"request":request, "user":user})