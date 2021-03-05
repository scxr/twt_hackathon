from fastapi import FastAPI
from endpoints import (hello_world_endpoint,
                       upload_csv_endpoint,
                       login_endpoint,
                       register_endpoint)
                       
import uvicorn
from db.base import Base, engine

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(hello_world_endpoint.router)
app.include_router(upload_csv_endpoint.router)
app.include_router(login_endpoint.router)
app.include_router(register_endpoint.router)
uvicorn.run(app)