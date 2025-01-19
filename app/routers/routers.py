import os
import aiofiles
from typing import Annotated, Union, Any


from fastapi import (APIRouter,
                     Header,
                     HTTPException,
                     UploadFile)

from ..models.models import (User,
                             UserCreate,
                             UserPublic,
                             Tweet,
                             TweetWithAuthor,
                             TweetIn,
                             Media,
                             Like,
                             SessionDep,
                             Followers,
    )

from sqlmodel import (select, delete)


app_router = APIRouter()


@app_router.get("/users/me", response_model=dict[str, Union[UserPublic, Any]])
async def read_item(session: SessionDep, api_key: Annotated[str | None, Header()] = None):
    user = session.scalars(select(User).where(User.api_key == api_key)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": True,
            "user": user}


@app_router.post("/tweets")
def tweet_add(tweet: TweetIn, session: SessionDep,
              api_key: Annotated[str | None, Header()] = None):

    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    links = session.scalars(select(Media.file_path)\
                            .filter(Media.id.in_(tweet.tweet_media_ids)))

    tweet_create = Tweet(tweet_data=tweet.tweet_data,
                               user_id=user_id,
                               links=links)

    session.add(tweet_create)
    session.commit()
    session.refresh(tweet_create)
    return {"result": True, "tweet_id": tweet_create.id}


@app_router.get("/tweets",
                response_model=dict[str, Union[list[TweetWithAuthor], Any]])
async def tweets_get(*, session: SessionDep):
    tweets = session.exec(select(Tweet)).all()
    return {"result": True, "tweets": tweets}


@app_router.post("/medias")
async def media_add(session: SessionDep,
                    file: UploadFile | None = None) -> dict:

    file_path = os.path.join('../app/templates/pictures', os.path.basename(file.filename))
    media_file = await file.read()

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(media_file)

    media_f = Media(file_path=file_path)
    session.add(media_f)
    session.commit()
    session.refresh(media_f)
    return {"result": True,
            "media_id": media_f.id}


@app_router.delete("/tweets/{id}")
async def tweet_delete(id, session: SessionDep,
                       api_key: Annotated[str | None, Header()] = None) -> dict:

    user_id = session.scalars(select(User.id).where(User.api_key==api_key)).one_or_none()
    if user_id is None:
        raise HTTPException(status_code=404, detail="Item not found")

    tweet_user_id = session.scalars(select(Tweet.user_id).where(Tweet.id==id)).one()
    if user_id == tweet_user_id:
        media_links = session.scalars(select(Tweet.links).where(Tweet.id==id)).one_or_none()
        session.exec(delete(Media).where(Media.file_path.in_(media_links)))
        session.exec(delete(Tweet).where(Tweet.id==id))
        session.commit()
        return {"result": True}
    else:
        raise HTTPException(status_code=404, detail="Item not deleted")


@app_router.post("/tweets/{id}/likes")
async def tweet_like_add(id, session: SessionDep,
                         api_key: Annotated[str | None, Header()] = None) -> dict:

    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    db_like = Like(user_id = user_id, tweet_id = id)
    session.add(db_like)
    session.commit()
    session.refresh(db_like)
    return {"result": True}


@app_router.delete("/tweets/{id}/likes")
async def tweet_like_delete(id, session: SessionDep,
                            api_key: Annotated[str | None, Header()] = None) -> dict:
    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    session.exec(delete(Like).where(Like.tweet_id==id).where(Like.user_id==user_id))
    session.commit()
    return {"result": True}


@app_router.post("/users/{id}/follow")
async def user_follow_add(id: int, session: SessionDep,
              api_key: Annotated[str | None, Header()] = None) -> dict:

    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()

    follower = Followers(follower_user_id=id,
                         follower_id=user_id)

    session.add(follower)
    session.commit()
    return {"result": True}


@app_router.delete("/users/{id}/follow")
async def user_follow_delete(id, session: SessionDep,
                             api_key: Annotated[str | None, Header()] = None) -> dict:
    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    session.exec(delete(Followers).where(Followers.follower_user_id==id)\
                 .where(Followers.follower_id==user_id))

    session.commit()

    return {"result": True}


@app_router.get("/users/{id}",
                response_model=dict[str, Union[UserPublic, Any]])
async def user_get(id, session: SessionDep):
    user = session.exec(select(User).where(User.id==id)).one_or_none()
    return {"result": True,
            "user": user}


@app_router.get("/users/")
def get_users(session: SessionDep) -> list[UserPublic]:
    users = session.exec(select(User)).all()
    return users


@app_router.post("/users/")
def create_user(user: UserCreate, session: SessionDep):
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
