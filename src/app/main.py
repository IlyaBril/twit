import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.models import create_db_and_tables
from app.routers.medias import app_medias
from app.routers.routers import app_init
from app.routers.tweets import app_tweets
from app.routers.users import app_users

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

root_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(root_dir, "templates")
js_directory = os.path.join(template_folder, "js")
css_directory = os.path.join(template_folder, "css")
pictures_directory = os.path.join(root_dir, "templates/pictures")

templates = Jinja2Templates(directory=template_folder)


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(app_init, prefix="/init")
app.include_router(app_users, prefix="/api/users")
app.include_router(app_tweets, prefix="/api/tweets")
app.include_router(app_medias, prefix="/api/medias")

app.mount("/templates", StaticFiles(directory=template_folder), name="templates")
app.mount("/css", StaticFiles(directory=css_directory), name="css")
app.mount("/js", StaticFiles(directory=js_directory), name="js")
app.mount("/pictures", StaticFiles(directory=pictures_directory), name="pictures")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/test")
async def welcome() -> dict:
    return {"message": "Hello"}
