import json

import pytest


def test_create_users(test_app_with_db_noauth):
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

    assert response.status_code == 201


#    user_id = response.json()["id"]
#    response = test_app_with_db_noauth.delete(f"/users/{user_id}/")
#    assert response.status_code == 200


def test_read_users_auth(test_app_with_db_auth):

    payload = {"username": "authtestuser", "password": "supersecretpassword"}
    response = test_app_with_db_auth.post("/token", data=payload)
    token = response.json()["access_token"]
    assert response.status_code == 200
    print(token)
    headersAuth = {"Authorization": "Bearer " + str(token)}
    print(headersAuth)
    response = test_app_with_db_auth.get("/users/", headers=headersAuth)
    assert response.status_code == 200


def test_create_users_invalid_json(test_app_with_db_noauth):
    response = test_app_with_db_noauth.post("/users/", data=json.dumps({}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "plain_password"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_read_user(test_app_with_db_noauth):
    response = test_app_with_db_noauth.post(
        "/users/",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": True,
                "plain_password": "supersecretpassword",
            }
        ),
    )
    user_id = response.json()["id"]

    response = test_app_with_db_noauth.get(f"/users/{user_id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == user_id
    assert response_dict["username"] == "testuser"
    assert response_dict["email"] == "testuser@example.com"
    assert response_dict["full_name"] == "Test User"
    assert response_dict["disabled"] == True
    assert response_dict["hashed_password"]
    assert response_dict["created_at"]

    response = test_app_with_db_noauth.delete(f"/users/{user_id}/")
    assert response.status_code == 200


def test_read_user_incorrect_id(test_app_with_db_noauth):
    response = test_app_with_db_noauth.get("/users/9999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_read_all_users(test_app_with_db_noauth):
    response = test_app_with_db_noauth.post(
        "/users/",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": True,
                "plain_password": "supersecretpassword",
            }
        ),
    )
    user_id = response.json()["id"]

    response = test_app_with_db_noauth.get("/users/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == user_id, response_list))) == 1

    response = test_app_with_db_noauth.delete(f"/users/{user_id}/")
    assert response.status_code == 200


def test_remove_user(test_app_with_db_noauth):
    response = test_app_with_db_noauth.post(
        "/users/",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": True,
                "plain_password": "supersecretpassword",
            }
        ),
    )
    user_id = response.json()["id"]

    response = test_app_with_db_noauth.delete(f"/users/{user_id}/")
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict["id"] == user_id
    assert response_dict["username"] == "testuser"
    assert response_dict["email"] == "testuser@example.com"
    assert response_dict["full_name"] == "Test User"
    assert response_dict["disabled"] == True


def test_remove_user_incorrect_id(test_app_with_db_noauth):
    response = test_app_with_db_noauth.delete("/users/9999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user(test_app_with_db_noauth):
    response = test_app_with_db_noauth.post(
        "/users/",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": True,
                "plain_password": "supersecretpassword",
            }
        ),
    )
    user_id = response.json()["id"]

    response = test_app_with_db_noauth.put(
        f"/users/{user_id}/",
        data=json.dumps(
            {
                "username": "testuserupdated",
                "email": "testuser.updatedr@example.com",
                "full_name": "Test User Updated",
                "disabled": False,
                "plain_password": "updated_supersecretpassword",
            }
        ),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == user_id
    assert response_dict["username"] == "testuserupdated"
    assert response_dict["email"] == "testuser.updatedr@example.com"
    assert response_dict["full_name"] == "Test User Updated"
    assert response_dict["disabled"] == False

    response = test_app_with_db_noauth.delete(f"/users/{user_id}/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "user_id, payload, status_code, detail",
    [
        [
            999,
            {
                "username": "testuserupdated",
                "email": "testuser.updatedr@example.com",
                "full_name": "Test User Updated",
                "disabled": False,
                "plain_password": "updated_supersecretpassword",
            },
            404,
            "User not found",
        ],
        [
            0,
            {
                "username": "testuserupdated",
                "email": "testuser.updatedr@example.com",
                "full_name": "Test User Updated",
                "disabled": False,
                "plain_password": "updated_supersecretpassword",
            },
            422,
            [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "loc": ["body", "username"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "plain_password"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
        [
            1,
            {
                "username": "testuserupdated",
                "email": "testuser.updatedr@example.com",
                "full_name": "Test User Updated",
                "disabled": False,
                "plain_password": "updated_supersecretpassword",
            },
            404,
            "User not found",
        ],
    ],
)
def test_update_user_invalid(
    test_app_with_db_noauth, user_id, payload, status_code, detail
):
    response = test_app_with_db_noauth.put(
        f"/users/{user_id}/", data=json.dumps(payload)
    )
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_user_invalid_username(test_app_with_db_noauth):
    response = test_app_with_db_noauth.post(
        "/users/",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": True,
                "plain_password": "supersecretpassword",
            }
        ),
    )
    user_id = response.json()["id"]

    response = test_app_with_db_noauth.put(
        f"/users/{user_id}/",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "testuser@example.com",
                "full_name": "Test User",
                "disabled": True,
                "plain_password": "supersecretpassword",
            }
        ),
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "must be alphanumeric",
                "type": "assertion_error",
            }
        ]
    }

    response = test_app_with_db_noauth.delete(f"/users/{user_id}/")
    assert response.status_code == 200
