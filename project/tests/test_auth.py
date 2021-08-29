import json


def test_create_testuser(test_app_with_db_noauth) -> str:

    response = test_app_with_db_noauth.post(
        "/users/",
        data=json.dumps(
            {
                "username": "authtestuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": False,
                "plain_password": "supersecretpassword",
            }
        ),
    )

    user_id = response.json()["id"]
    return user_id


def test_auth_users(test_app_with_db_auth):

    payload = {"username": "authtestuser", "password": "supersecretpassword"}
    response = test_app_with_db_auth.post("/token", data=payload)
    token = response.json()["access_token"]
    assert response.status_code == 200
    print(token)
    headersAuth = {"Authorization": "Bearer " + str(token)}
    print(headersAuth)
    response = test_app_with_db_auth.get("/users/", headers=headersAuth)
    assert response.status_code == 200


def test_auth_wrong_user(test_app_with_db_auth):

    payload = {"username": "wrongauthtestuser", "password": "supersecretpassword"}
    response = test_app_with_db_auth.post("/token", data=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_auth_wrong_password(test_app_with_db_auth):

    payload = {"username": "authtestuser", "password": "wrongsupersecretpassword"}
    response = test_app_with_db_auth.post("/token", data=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_auth_disable_user(test_app_with_db_noauth):
    response = test_app_with_db_noauth.get("/users/")
    assert response.status_code == 200

    user_id = response.json()[0]["id"]

    response = test_app_with_db_noauth.put(
        f"/users/{user_id}/",
        data=json.dumps(
            {
                "username": "authtestuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": True,
                "plain_password": "supersecretpassword",
            }
        ),
    )
    assert response.status_code == 200


def test_auth_disabled_user(test_app_with_db_auth):

    payload = {"username": "authtestuser", "password": "supersecretpassword"}
    response = test_app_with_db_auth.post("/token", data=payload)
    token = response.json()["access_token"]
    assert response.status_code == 200
    print(token)
    headersAuth = {"Authorization": "Bearer " + str(token)}
    print(headersAuth)
    response = test_app_with_db_auth.get("/users/", headers=headersAuth)
    assert response.status_code == 400
    assert response.json() == {"detail":"Inactive user"}
    


def test_delete_testuser(test_app_with_db_noauth) -> None:
    response = test_app_with_db_noauth.get("/users/")
    assert response.status_code == 200
    user_id = response.json()[0]["id"]

    response = test_app_with_db_noauth.delete(f"/users/{user_id}/")
    assert response.status_code == 200
