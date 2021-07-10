import json

import pytest


def test_create_users(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_users_invalid_json(test_app):
    response = test_app.post("/users/", data=json.dumps({}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"url": "https://foo.bar"})
    )
    user_id = response.json()["id"]

    response = test_app_with_db.get(f"/users/{user_id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == user_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["name"]
    assert response_dict["created_at"]


def test_read_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/users/9999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_read_all_users(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"url": "https://foo.bar"})
    )
    user_id = response.json()["id"]

    response = test_app_with_db.get("/users/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == user_id, response_list))) == 1


def test_remove_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"url": "https://foo.bar"})
    )
    user_id = response.json()["id"]

    response = test_app_with_db.delete(f"/users/{user_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "url": "https://foo.bar"}


def test_remove_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/users/9999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users/", data=json.dumps({"url": "https://foo.bar"})
    )
    user_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/users/{user_id}/",
        data=json.dumps({"url": "https://foo.bar", "name": "updated"}),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == user_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["name"] == "updated"
    assert response_dict["created_at"]


@pytest.mark.parametrize(
    "user_id, payload, status_code, detail",
    [
        [999, {"url": "https://foo.bar", "name": "updated!"}, 404, "User not found"],
        [
            0,
            {"url": "https://foo.bar", "name": "updated"},
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
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
        [
            1,
            {"url": "https://foo.bar"},
            422,
            [
                {
                    "loc": ["body", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        ],
    ],
)
def test_update_user_invalid(test_app_with_db, user_id, payload, status_code, detail):
    response = test_app_with_db.put(f"/users/{user_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_user_invalid_url(test_app):
    response = test_app.put(
        "/users/1/", data=json.dumps({"url": "invalid://url", "name": "updated!"})
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
