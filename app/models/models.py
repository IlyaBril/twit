from sqlmodel import JSON, SQLModel, Field, Column, Relationship, ARRAY
from sqlmodel import Session, create_engine, select
from typing import Optional, List, Annotated

from fastapi import Depends, FastAPI, HTTPException, Query



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class TweetBase(SQLModel):  
    tweet_data: str = Field(index=True)
    #tweet_media_ids: ARRAY = Field()

    
class Tweet(TweetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="tweet")


class TweetCreate(TweetBase):
    pass


class TweetPublic(TweetBase):
    id: int


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    api_key: str = Field()
    tweet: Tweet = Relationship(back_populates="user")

    class Config:
        schema_extra = {
            "example": {
                "name": "name"
            }
        }


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

