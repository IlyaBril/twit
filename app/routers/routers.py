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
logging.basicConfig(filename='myapp.log')

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
def tweet_add(tweet: TweetCreate, session: SessionDep, request: Request):

    api_key = request.headers["api-key"]
    #api_key = 'test'
    user_id = session.scalars(select(User.id).where(User.api_key==api_key)).one()
    tweet.user_id = user_id
    db_tweet = Tweet.model_validate(tweet)
    session.add(db_tweet)
    session.commit()
    session.refresh(db_tweet)
    return {"result": "true", "tweet_id": db_tweet.user_id}


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


@app_router.post("/users/")
def create_hero(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
#
#
@app_router.get("/users/")
def get_users(session: SessionDep) -> list[User]:
    users = session.exec(select(User)).all()
    return users
#
#
#
# @app_router.post("/users/")
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
