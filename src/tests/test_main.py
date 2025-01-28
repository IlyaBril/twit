from fastapi.testclient import TestClient


def test_root_2(client):
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_create_user(client: TestClient):
    client.post("/api/users", json={'id': 1, "name": "name_1", "api_key": "test"})
    response = client.get("/api/users/1")

    data = response.json()

    assert response.status_code == 200
    assert data == {
        "result": True,
        "user": {
            "id": 1,
            "name": "name_1",
            "followers": [],
            "following": []
        }
    }


def test_get_user_me(client: TestClient):
    response = client.get("/api/users/me", headers={"api-key": "test"})
    data = response.json()

    assert response.status_code == 200
    assert data == {"result": True,
                    "user": {
                        "id": 1,
                        "name":"name_1",
                        "followers":[],
                        "following":[]
                    }
                    }

def test_create_user_2(client: TestClient):
    client.post("/api/users", json={'id': 2, "name": "name_1", "api_key": "test_2"})
    response = client.get("/api/users/2")

    data = response.json()

    assert response.status_code == 200
    assert data == {
        "result": True,
        "user": {
            "id": 2,
            "name": "name_1",
            "followers": [],
            "following": []
        }
    }


def test_create_tweet_user_1(client: TestClient):
    response = client.post("/api/tweets",
                headers={"api-key": "test"},
                json={"tweet_data": "tweet_data_1",
                      "links": [],
                      "tweet_media_ids": []})

    assert response.status_code == 200
    assert response.json() == {"result": True, "tweet_id": 1}


def test_get_tweets(client: TestClient):
    response = client.get("/api/tweets")
    data = response.json()

    assert response.status_code == 200
    assert data == {"result": True,
                    "tweets": [
                        {
                            "content": "tweet_data_1",
                            "attachments": [],
                            "id": 1,
                            "author": {
                                "name": "name_1",
                                "id": 1
                            },
                            "likes": []
                        }
                    ]
                    }


def test_create_like(client: TestClient):
    response = client.post("/api/tweets/1/likes", headers={"api-key": "test"})
    data = response.json()

    assert response.status_code == 200
    assert data == {"result": True}


def test_delete_like(client: TestClient):
    response = client.delete("/api/tweets/1/likes", headers={"api-key": "test"})
    data = response.json()

    assert response.status_code == 200
    assert data == {"result": True}


def test_delete_tweets(client: TestClient):
    response = client.delete("/api/tweets/1", headers={"api-key": "test"})
    data = response.json()

    assert response.status_code == 200
    assert data == {"result": True}


def test_follow_user(client: TestClient):
    response = client.post("/api/users/2/follow", headers={"api-key": "test"})
    data = response.json()

    assert response.status_code == 200
    assert data == {"result": True}


def test_unfollow_user(client: TestClient):
    response = client.delete("/api/users/2/follow", headers={"api-key": "test"})
    data = response.json()

    assert response.status_code == 200
    assert data == {"result": True}

