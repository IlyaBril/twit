from typing import Annotated, Any, Optional

from fastapi import Depends
from sqlmodel import (
    ARRAY,
    Column,
    Field,
    LargeBinary,
    Relationship,
    Session,
    SQLModel,
    String,
    create_engine,
)

engine = create_engine("postgresql+psycopg2://postgres:postgres@my_db:5432/twit_db")


class FollowersBase(SQLModel):
    pass


class Followers(FollowersBase, table=True):
    __tablename__ = "followers_table"
    id: int | None = Field(default=None, primary_key=True)
    follower_user_id: int = Field(default=None, foreign_key="user.id")
    follower_id: int = Field(default=None, foreign_key="user.id")


class UserBase(SQLModel):
    name: str = Field(index=True)
    id: int | None = Field(
        default=None,
        primary_key=True,
        alias="user_id",
        schema_extra={"serialization_alias": "user_id"},
    )


class User(UserBase, table=True):
    __tablename__ = "user"

    api_key: str = Field(unique=True)
    tweet: Optional[list["Tweet"]] = Relationship(back_populates="author")

    followers: Optional[list["User"]] = Relationship(
        back_populates="following",
        sa_relationship_kwargs=dict(
            secondary="followers_table",
            primaryjoin="User.id == Followers.follower_user_id",
            secondaryjoin="User.id == Followers.follower_id",
        ),
    )

    following: Optional[list["User"]] = Relationship(
        back_populates="followers",
        sa_relationship_kwargs=dict(
            secondary="followers_table",
            primaryjoin="User.id == Followers.follower_id",
            secondaryjoin="User.id == Followers.follower_user_id",
        ),
    )


class UserTweet(UserBase):
    id: int


class UserPublic(UserBase):
    id: int
    followers: list["UserTweet"] | None = None
    following: list["UserTweet"] | None = None


class UserLike(UserBase):
    pass


class UserCreate(UserBase):
    api_key: str


class TweetBase(SQLModel):
    # model_config = ConfigDict(populate_by_name=True)
    tweet_data: Optional[str] = Field(
        alias="content", schema_extra={"serialization_alias": "content"}
    )

    links: Optional[list[str]] = Field(
        sa_column=Column(ARRAY(String)),
        default=None,
        schema_extra={"serialization_alias": "attachments"},
    )


class Tweet(TweetBase, table=True):
    __tablename__ = "tweet"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    author: "User" = Relationship(back_populates="tweet")
    likes: Optional[list["User"]] = Relationship(
        # back_populates="   ",
        sa_relationship_kwargs=dict(
            secondary="likes",
            primaryjoin="Tweet.id == Like.tweet_id",
            secondaryjoin="User.id == Like.user_id",
        )
    )


class TweetIn(TweetBase):
    tweet_data: str | None = None
    tweet_media_ids: Optional[list[int]] = None


class TweetPublic(TweetBase):
    id: Optional[int] = None


class TweetWithAuthor(TweetPublic):
    author: UserTweet | None = None
    likes: list["UserLike"] | None = None


class MediaBase(SQLModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    file_name: str | None = Field(default=None)


class Media(MediaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    file_body: Optional[Any] = Field(sa_column=Column(LargeBinary), default=None)


class MediaPublic(MediaBase):
    id: int


class LikeBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)


class Like(LikeBase, table=True):
    __tablename__ = "likes"
    tweet_id: int | None = Field(
        default=None, foreign_key="tweet.id", primary_key=True, ondelete="CASCADE"
    )


class LikePublic(LikeBase):
    user_id: int | None = None


class LikeCreate(LikeBase):
    user_id: int
    tweet_id: int


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
