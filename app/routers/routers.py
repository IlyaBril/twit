import logging
import os
import aiofiles
from typing import Annotated, Union, Any, List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import (APIRouter,
                     Request,
                     Header,
                     Depends,
                     File,
                     UploadFile)

from ..models.models import (User,
                             UserCreate,
                             Tweet,
                             TweetCreate,
                             TweetPublic,
                             TweetWithAuthor,
                             Media,
                             MediaCreate,
                             Like,
                             LikeCreate,
                             SessionDep)

from sqlmodel import (Field,
                      Session,
                      SQLModel,
                      create_engine,
                      select,
                      delete)

from sqlalchemy.orm import joinedload

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
    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    tweet.user_id = user_id

    links = session.scalars(select(Media.file_path)\
                            .filter(Media.id.in_(tweet.tweet_media_ids)))

    tweet.links = links

    db_tweet = Tweet.model_validate(tweet)
    session.add(db_tweet)
    session.commit()
    session.refresh(db_tweet)
    return {"result": "true", "tweet_id": db_tweet.id}


@app_router.get("/tweets",
                response_model=dict[str, Union[list[TweetWithAuthor],
                Any]])
#@app_router.get("/tweets", response_model=None)
async def tweets_get(*, session: SessionDep):
    #tweets = session.scalars(select(Tweet, User, Like).join_from(User, Like, isouter=True)).all()
    tweets = session.exec(select(Tweet)).all()

    #return tweets
    return {"result": "true", "tweets": tweets}


@app_router.post("/medias")
async def media_add(session: SessionDep,
                    request: Request,
                    file: UploadFile | None = None) -> dict:
    # api_key = request.headers["api-key"]
    api_key = 'test'

    file_path = os.path.join('./pictures/', os.path.basename(file.filename))
    media_file = await file.read()

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(media_file)

    media_f = Media(file_path=file_path)
    session.add(media_f)
    session.commit()
    session.refresh(media_f)
    return {"result": "true",
            "media_id": media_f.id}


@app_router.delete("/tweets/{id}")
async def tweet_delete(id, session: SessionDep) -> dict:
    # api_key = request.headers["api-key"]
    api_key = 'test'
    user_id = session.scalars(select(User.id).where(User.api_key==api_key)).one()
    tweet_user_id = session.scalars(select(Tweet.user_id).where(Tweet.id==id)).one()
    if user_id == tweet_user_id:
        session.exec(delete(Tweet).where(Tweet.id==id))
        #session.exec(delete(Tweet, id))
        session.commit()
    return {"result": "true"}


@app_router.post("/tweets/{id}/likes")
async def tweet_like_add(id, session: SessionDep,
                         request: Request) -> dict:
    # api_key = request.headers['api-key']
    api_key = "test_3"
    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()

    db_like = Like(user_id = user_id, tweet_id = id)

    session.add(db_like)
    session.commit()
    session.refresh(db_like)
    return {"result": True}


#@app.delete("/app/tweets/<id>/like")
#async def tweet_like_delete(id) -> dict:
#    return {"result": "true"}


#@app.post("/app/users/<id>/follow")
#async def user_follow_add(id):
#    return {"result": "true"}


#@app.delete("/app/users/<id>/follow")
#async def user_follow_delete(id):
#    return {"result": "true"}


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


@app_router.get("/users/")
def get_users(session: SessionDep) -> list[User]:
    users = session.exec(select(User)).all()
    return users


@app_router.post("/users/")
def create_user(user: UserCreate, session: SessionDep, request: Request):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app_router.get("/create_db")
def create_db(session: SessionDep):
    #create users
    user = User(name="name_1", api_key="test")
    session.add(user)
    for i in range(2, 5):
        name = f'name{i}'
        api_key = f'test_{i}'
        user = User(name=name, api_key=api_key)
        session.add(user)
    session.commit()

    #create tweets

    for i in range(2, 5):
        user_id = 1
        content = f"content{i}"
        #tweet = Tweet(user_id=user_id, content=content)
        tweet = Tweet(user_id=user_id, tweet_data=content)
        session.add(tweet)
    session.commit()

    #create likes

    like1 = Like(user_id=2, tweet_id=2)
    like2 = Like(user_id=2, tweet_id=3)

    session.add(like1)
    session.add(like2)

    session.commit()

    return {"result": True}