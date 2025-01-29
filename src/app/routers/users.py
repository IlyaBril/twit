from typing import Annotated, Any, Union

from fastapi import APIRouter, Header, HTTPException
from sqlmodel import delete, select

from app.models.models import Followers, SessionDep, User, UserCreate, UserPublic

app_users = APIRouter()


@app_users.get("/me", response_model=dict[str, Union[UserPublic, Any]])
async def read_item(
    session: SessionDep, api_key: Annotated[str | None, Header()] = None
):
    user = session.scalars(select(User).where(User.api_key == api_key)).one_or_none()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "User",
                "error_message": "User not found",
            },
        )

    return {"result": True, "user": user}


@app_users.get("/{id}", response_model=dict[str, Union[UserPublic, Any]])
async def user_get(id, session: SessionDep):
    user = session.scalars(select(User).where(User.id == id)).one_or_none()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "User",
                "error_message": "User not found",
            },
        )
    return {"result": True, "user": user}


@app_users.post("/{id}/follow")
async def user_follow_add(
    id: int, session: SessionDep, api_key: Annotated[str | None, Header()] = None
) -> dict:

    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    follower = Followers(follower_user_id=id, follower_id=user_id)

    session.add(follower)
    session.commit()
    return {"result": True}


@app_users.delete("/{id}/follow")
async def user_follow_delete(
    id, session: SessionDep, api_key: Annotated[str | None, Header()] = None
) -> dict:
    user_id = session.scalars(select(User.id).where(User.api_key == api_key)).one()
    session.execute(
        delete(Followers)
        .where(Followers.follower_user_id == id)
        .where(Followers.follower_id == user_id)
    )

    session.commit()
    return {"result": True}


@app_users.get("/", response_model=list[UserPublic] | None)
def get_users(session: SessionDep):
    return session.exec(select(User)).all()


@app_users.post("/")
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
