from pydantic import ConfigDict
from pydantic.alias_generators import to_pascal
from sqlmodel import (JSON,
                      SQLModel,
                      Field,
                      Column,
                      Relationship,
                      ARRAY,
                      String)

from sqlmodel import (Session,
                      create_engine,
                      select)

from typing import Optional, Annotated, List, Any

from fastapi import Depends, FastAPI, HTTPException, Query, Body

engine = create_engine('postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/twit_db')

class UserBase(SQLModel):
    name: str = Field(index=True)


class User(UserBase, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    tweet: Optional[list["Tweet"]] = Relationship(back_populates="author")
    likes: Optional["Like"] = Relationship(back_populates="namee")
    api_key: str = Field()


class UserPublic(UserBase):
    id: int


class UserLike(UserBase):
    user_id: int | None = id


class UserCreate(UserBase):
    api_key: str


class TweetBase(SQLModel):
    #model_config = ConfigDict(populate_by_name=True)

    #content: Optional[str] = Field(index=True, alias='tweet_data')
    tweet_data: Optional[str] = Field(alias='content',
                                      schema_extra={"serialization_alias": "content"})
    links: Optional[list[str]] = Field(sa_column=Column(ARRAY(String)),
                                       schema_extra={"serialization_alias": "attachments"})

    class Config:
        allow_population_by_field_name = True


class Tweet(TweetBase, table=True):
    __tablename__ = "tweet"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")

    author: "User" = Relationship(back_populates="tweet")
    likes: Optional[list["Like"]] = Relationship(back_populates="tweet",
                                                 cascade_delete=True)


    # class Config:
    #     arbitrary_types_allowed = True


class TweetCreate(TweetBase):
    user_id: Optional[int] = None
    tweet_data: str | None = None
    #content: str | None = None
    links: List[str] | None = None
    tweet_media_ids: Any


class TweetPublic(TweetBase):
    id: int



class TweetWithAuthor(TweetPublic):
    author: UserPublic | None = None
    likes: list["LikePublic"]
    name: str | None = None


class MediaBase(SQLModel):
    file_path: str | None = Field(default=None)


class Media(MediaBase, table=True):
    id: int = Field(default=None, primary_key=True)


class MediaCreate(MediaBase):
    pass


class MediaPublic(MediaBase):
    id: int


class LikeBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    # tweet: "Tweet" = Relationship(back_populates="likes")


class Like(LikeBase, table=True):
     __tablename__ = "likes"
     #id: int = Field(default=None, primary_key=True)
     #user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
     tweet_id: int | None = Field(default=None, foreign_key="tweet.id", primary_key=True,
                                  ondelete="CASCADE")

     tweet: "Tweet" = Relationship(back_populates="likes")
     namee: "User" = Relationship(back_populates="likes")


class LikePublic(LikeBase):
    user_id: int | None = None
    # plug. remove when issue solved
    name : str | None = "to be changed"
    #namee: UserPublic


class LikeCreate(LikeBase):
    user_id: int
    tweet_id: int


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

