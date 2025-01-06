from pydantic import ConfigDict, BaseModel
from pydantic.alias_generators import to_pascal
from sqlalchemy.orm import mapped_column, relationship
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


class FollowersBase(SQLModel):
    pass


class Followers(FollowersBase, table=True):
    __tablename__ = 'followers_table'
    id: int | None = Field(default=None, primary_key=True)
    follower_user_id: int = Field(default=None, foreign_key="user.id")
    follower_id: int = Field(default=None, foreign_key="user.id")




class UserBase(SQLModel):
    name: str = Field(index=True)


class User(UserBase, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    api_key: str = Field()
    tweet: Optional[list["Tweet"]] = Relationship(back_populates="author")
    likes: Optional["Like"] = Relationship(back_populates="namee")

    followers: Optional[list["User"]] = Relationship(
        back_populates='following',
        sa_relationship_kwargs=dict(
            secondary="followers_table",
            primaryjoin="User.id == Followers.follower_user_id",
            secondaryjoin="User.id == Followers.follower_id"))


    following: Optional[list["User"]] = Relationship(
        back_populates="followers",
        sa_relationship_kwargs=dict(
            secondary="followers_table",
            primaryjoin="User.id == Followers.follower_id",
            secondaryjoin="User.id == Followers.follower_user_id"))


class UserTweet(UserBase):
    id: int


class UserPublic(UserBase):
    id: int
    followers: list["UserBase"] | None = None




class UserLike(UserBase):
    user_id: int | None = id


class UserCreate(UserBase):
    api_key: str


class TweetBase(SQLModel):
    tweet_data: Optional[str] = Field(alias='content',
                                      schema_extra={"serialization_alias": "content"})

    class Config:
        allow_population_by_field_name = True


class Tweet(TweetBase, table=True):
    __tablename__ = "tweet"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")

    links: Optional[list[str]] = Field(sa_column=Column(ARRAY(String)), default=None,
                                       schema_extra={"serialization_alias": "attachments"})

    author: "User" = Relationship(back_populates="tweet")
    likes: Optional[list["Like"]] = Relationship(back_populates="tweet",
                                                 cascade_delete=True)


class TweetIn(TweetBase):
    tweet_data: str | None = None
    tweet_media_ids: Optional[list[int]] = None


class TweetCreate(TweetIn):
    user_id: Optional[int] = None
    links: List[str] | None = None


class TweetPublic(TweetBase):
    id: int


class TweetWithAuthor(TweetPublic):
    author: UserTweet | None = None
    likes: list["LikePublic"] | None = None
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







# class FollowersCreate(FollowersBase):
#     follower_user_id: int
#     follower_id: int


# class FollowersPublic(FollowersBase):
#     follower_id: int
#     follower: Optional["UserBase"] = None
#     #follower: Optional["UserPublic"] = None
#
#
# class FollowingBase(SQLModel):
#     pass


# class Following(FollowingBase, table=True):
#     __tablename__ = 'following'
#     id: int | None = Field(default=None, primary_key=True)
#     following_user_id: int = Field(default=None, foreign_key="user.id")
#     following_id: int = Field(default=None)
#     #following_user: "User" = Relationship(back_populates="following_user")
#     following: Optional["User"] = Relationship(back_populates="following")
#
#
# class FollowingCreate(FollowingBase):
#     follow_id: int
#     following_id: int
#
#
# class FollowingPublic(FollowingBase):
#     following: list["UserFollowing"] | None = None


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

