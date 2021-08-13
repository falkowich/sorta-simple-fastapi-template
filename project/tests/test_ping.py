def test_ping(test_app_with_db):
    response = test_app_with_db.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong", "testing": True}
