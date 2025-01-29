from typing import Annotated, Any, Union

from fastapi import APIRouter, Header, HTTPException
from sqlmodel import delete, select

from app.models.models import (
    Like,
    Media,
    SessionDep,
    Tweet,
    TweetIn,
    TweetWithAuthor,
    User,
)

app_tweets = APIRouter()


@app_tweets.get("/", response_model=dict[str, Union[list[TweetWithAuthor], Any]])
async def tweets_get(*, session: SessionDep):
    tweets = session.exec(select(Tweet)).all()
    return {"result": True, "tweets": tweets}


@app_tweets.post("/")
def tweet_add(
    tweet: TweetIn, session: SessionDep, api_key: Annotated[str | None, Header()] = None
):
    if api_key is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = session.scalars(
        select(User.id).where(User.api_key == api_key)
    ).one_or_none()
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")

    links = []
    if tweet.tweet_media_ids:
        for i in tweet.tweet_media_ids:
            links.append(f"/api/medias/{i}")

    tweet_create = Tweet(tweet_data=tweet.tweet_data, user_id=user_id, links=links)

    session.add(tweet_create)
    session.commit()
    session.refresh(tweet_create)

    return {"result": True, "tweet_id": tweet_create.id}


@app_tweets.delete("/{id}")
async def tweet_delete(
    id, session: SessionDep, api_key: Annotated[str | None, Header()] = None
) -> dict:

    user_id = session.scalars(
        select(User.id).where(User.api_key == api_key)
    ).one_or_none()
    if user_id is None:
        raise HTTPException(status_code=404, detail="Incorrect User")

    tweet_user_id = session.scalars(select(Tweet.user_id).where(Tweet.id == id)).one()
    if user_id == tweet_user_id:
        media_links = session.scalars(
            select(Tweet.links).where(Tweet.id == id)
        ).one_or_none()

        if media_links:
            for media_id in media_links:
                media_id = media_id.split("/")[-1]
                session.execute(delete(Media).where(Media.id == media_id))
        session.execute(delete(Tweet).where(Tweet.id == id))
        session.commit()
        return {"result": True}
    else:
        raise HTTPException(status_code=404, detail="Item not deleted")


@app_tweets.post("/{id}/likes")
async def tweet_like_add(
    id, session: SessionDep, api_key: Annotated[str | None, Header()] = None
) -> dict:

    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    db_like = Like(user_id=user_id, tweet_id=id)
    session.add(db_like)
    session.commit()
    session.refresh(db_like)
    return {"result": True}


@app_tweets.delete("/{id}/likes")
async def tweet_like_delete(
    id, session: SessionDep, api_key: Annotated[str | None, Header()] = None
) -> dict:
    user_id = session.scalars(
        select(User.id).where(User.api_key == api_key)
    ).one_or_none()
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.execute(
        delete(Like).where(Like.tweet_id == id).where(Like.user_id == user_id)
    )
    session.commit()
    return {"result": True}
