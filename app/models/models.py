from sqlmodel import JSON, SQLModel, Field, Column, Relationship, ARRAY, Integer
from sqlmodel import Session, create_engine, select
from typing import Optional, Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query

engine = create_engine('postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/twit_db')


class UserBase(SQLModel):
    name: str = Field(index=True)


class User(UserBase, table=True):
    __tablename__ = "user"
    id: int = Field(primary_key=True)
    api_key: str = Field()
    tweet: "Tweet" = Relationship(back_populates="author")


    class Config:
        schema_extra = {
            "example": {
                "name": "name"
            }
        }


class UserPublic(UserBase):
    id: int


class TweetBase(SQLModel):
    content: Optional[str] = Field(index=True)
    tweet_media_ids: List[int] = Field(sa_column=Column(ARRAY(Integer)))


class Tweet(TweetBase, table=True):
    __tablename__ = "tweet"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    author: "User" = Relationship(back_populates="tweet")

    class Config:
        arbitrary_types_allowed = True


class TweetCreate(TweetBase):
    user_id: Optional[int] = None
    tweet_data: str | None = None
    content: str | None = None
    tweet_media_ids: List[int]


class TweetPublic(TweetBase):
    author : UserPublic


class TweetResponse(TweetPublic):
    result: str | None
    items : TweetPublic


class MediaBase(SQLModel):
    image: bytes | None = None


class Media(MediaBase, table=True):
    media_id: int = Field(default=None, primary_key=True)
    image: bytes = Field(default=None)


class MediaCreate(MediaBase):
    pass


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

