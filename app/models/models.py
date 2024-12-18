from sqlmodel import JSON, SQLModel, Field, Column, Relationship, ARRAY
from typing import Optional, List
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query

from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    api_key: str = Field()
    tweet: list["Tweet"] = Relationship(back_populates="user")

    class Config:
        schema_extra = {
            "example": {
                "name": "name"
            }
        }


class Tweet(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    tweet_data: str = Field(index=True)
    tweet_media_ids: ARRAY
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="tweet")

    #class Config: schema_extra = {"example": {"name": "name"}}


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

