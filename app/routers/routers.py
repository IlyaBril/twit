import logging
from typing import Annotated, Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import (APIRouter,
                     Request,
                     Header,
                     Depends,
                     UploadFile)

from ..models.models import (User,
                             Tweet,
                             TweetCreate,
                             TweetPublic,
                             TweetResponse,
                             Media,
                             MediaCreate,
                             SessionDep)

from sqlmodel import (Field,
                      Session,
                      SQLModel,
                      create_engine,
                      select)



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

    #api_key = request.headers["api-key"]
    api_key = 'test'
    user_id = session.scalars(select(User.id).where(User.api_key==api_key)).one()
    tweet.user_id = user_id
    tweet.content = tweet.tweet_data
    db_tweet = Tweet.model_validate(tweet)
    session.add(db_tweet)
    session.commit()
    session.refresh(db_tweet)
    return {"result": "true", "tweet_id": db_tweet.id}


@app_router.get("/tweets", response_model=dict[str, Union[list[TweetPublic], str]])
#@app_router.get("/tweets")
async def tweets_get(*, session: SessionDep):
    tweets = session.scalars(select(Tweet, User).join(User)).all()
    #tweets = session.scalars(select(Tweet)).all()
    #return tweets
    return {"result": "true", "tweets": tweets}


@app_router.post("/medias")
async def media_add(session: SessionDep,
                    request: Request,
                    file: UploadFile | None = None) -> dict:
    # api_key = request.headers["api-key"]
    api_key = 'test'

    media_file = await file.read()
    media_f = Media(image = media_file)

    session.add(media_f)
    session.commit()
    session.refresh(media_f)

    return {"result": "true",
            "media_id": media_f.media_id}


#@app.delete("tweets/<id>")
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
def create_user(user: User, session: SessionDep) -> User:
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
