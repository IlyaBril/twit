import uvicorn
from fastapi import APIRouter, Request, Header
from sqlmodel import Field, Session, SQLModel, create_engine, select

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import logging
from fastapi import FastAPI
from .models.models import create_db_and_tables
from .routers.routers import app_router


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

templates = Jinja2Templates(directory="templates")

app = FastAPI()



app.include_router(app_router,  prefix="/api")

app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")
app.mount("/templates", StaticFiles(directory="templates"))


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    #id = request.headers["api-key"]
    return templates.TemplateResponse(
        request=request, name="index.html", headers={"api-key": "test"}
    )


@app.get("/test")
async def welcome() -> dict:
    return {"message": "Hello"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

