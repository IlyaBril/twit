import logging

from fastapi import APIRouter, Request, Header
from ..models.models import User, Tweet, TweetCreate, SessionDep
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app_router = APIRouter()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app_router.get("/users/me")
async def read_item(request: Request):
    #     """
    #     {"result":"true",
    #      "user": {"id":"int", "name":"str", "followers":[{"id":"int", "name":"str"}],
    #               "following":[{"id":"int", "name":"str"}]
    #               }
    #     }
    #     """
    id = request.headers["api-key"]
    return {"result": "true",
            "user": {"id": id,
                     "name": "name",
                     "followers": [],
                     "following": [],
                     }
            }


@app_router.post("/tweets")
def tweet_add(request: Request, session: SessionDep):
    print('test')
    api_key = request.headers["api-key"]
    tweet_data = request.form
    tweet_dat = tweet_data["tweet_data"]
    user_id = session.execute(select(User.id).where(User.api_key==api_key)).fetchone()
    logger.info('user id {}'.format(user_id))
    tweet_create = TweetCreate(user_id=user_id, tweet_data=tweet_dat)
    session.add(tweet_create)
    session.commit()
    session.refresh(tweet_create)
    return {"result": "true", "tweet_id": 1}


@app_router.get("/tweets")
async def tweets_get():
    return {
        "result": "true2",
        "tweets": [
            {
                "id": 1,
                "content": "hi",
                "attachements": [],
                "author": {
                    "id": 1,
                    "name": "test"
                    },
                "likes":[
                    ]
                }
            ]
        }





# @app.post("/users/")
# def create_hero(user: User, session: SessionDep) -> User:
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user
#


#@app.post("/app/medias")
#async def media_add() -> dict:
#    return {"result": "true",
#            "media_id": "int"}


#@app.delete("/app/tweets/<id>")
#async def tweet_delete(id) -> dict:
#    return {"result": "true"}


#@app.post("/app/tweets/<id>/like")
#async def tweet_like_add(id) -> dict:
#    return {"result": "true"}


#@app.delete("/app/tweets/<id>/like")
#async def tweet_like_delete(id) -> dict:
#    return {"result": "true"}


#@app.post("/app/users/<id>/follow")
#async def user_follow_add(id):
#    return {"result": "true"}


#@app.delete("/app/users/<id>/follow")
#async def user_follow_delete(id):
#    return {"result": "true"}





# @app.post("/users/")
# def create_hero(user: User, session: SessionDep) -> User:
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user
#
#
# @app.get("/users/")
# def get_users(session: SessionDep) -> list[User]:
#     users = session.exec(select(User)).all()
#     return users
#
#
#
# @router.post("/app/users/")
# async def user_follow_add():
#     return {"result": "all users"}
#
#
#
# @app_router.get("/app/users/<id>")
# async def user_get():
#     """
#     {"result":"true",
#      "user": {"id":"int", "name":"str",
#               "followers":[{"id":"int", "name":"str"}],
#               "following":[{"id":"int", "name":"str"}]
#               }
#     }
#     """
#     return {"result": "true"}
