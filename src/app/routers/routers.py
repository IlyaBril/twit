from fastapi import (APIRouter)

from app.models.models import (User,
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

app_init = APIRouter()


@app_init.get("/create_db")
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
        tweet = Tweet(api_key="test_2", tweet_data=content)
        session.add(tweet)
    session.commit()

    #create likes

    like1 = Like(api_key="test_2", tweet_id=2)
    like2 = Like(api_key="test_2", tweet_id=3)

    session.add(like1)
    session.add(like2)

    session.commit()

    return {"result": True}
