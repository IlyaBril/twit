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
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)



app.include_router(app_router,  prefix="/api")

app.mount("/app/templates/css", StaticFiles(directory="../app/templates/css"), name="css")
app.mount("/app/templates/js", StaticFiles(directory="../app/templates/js"), name="js")
app.mount("/app/templates", StaticFiles(directory="../app/templates"), name="pictures")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    #id = request.headers["api-key"]
    return templates.TemplateResponse(
        request=request, name="index.html", headers={"api-key": "test"}
    )


@app.get("/test")
async def welcome() -> dict:
    return {"message": "Hello"}


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()



