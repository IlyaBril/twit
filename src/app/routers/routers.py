from fastapi import APIRouter

from app.models.models import Like, SessionDep, Tweet, User

app_init = APIRouter()


@app_init.get("/create_db")
def create_db(session: SessionDep):
    # create users
    user = User(name="name_1", api_key="test")
    session.add(user)
    for i in range(2, 5):
        name = f"name{i}"
        api_key = f"test_{i}"
        user = User(name=name, api_key=api_key)
        session.add(user)
    session.commit()

    # create tweets

    for i in range(2, 5):
        content = f"content{i}"
        tweet = Tweet(api_key="test_2", tweet_data=content)
        session.add(tweet)
    session.commit()

    return {"result": True}
