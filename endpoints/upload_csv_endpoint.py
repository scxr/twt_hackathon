from fastapi import File, UploadFile, APIRouter, Request
from fastapi.templating import Jinja2Templates
import os
router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.post('/upload_file')
async def create_upload_file(file : UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        path = os.getcwd() + '\\upload_files\\' + file.filename
    else:
        return {"error":"file extension must be .csv"}
    print(os.getcwd())
    with open(path, 'wb+') as f:
        f.write(file.file.read())
        f.close()
    return {"filename":file.filename}

@router.get('/upload_file')
async def get_upload_file(request: Request):
    return templates.TemplateResponse("upload_csv.html", {"request":request})