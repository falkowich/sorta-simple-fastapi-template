def test_ping(test_app_with_db_noauth):
    response = test_app_with_db_noauth.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong", "testing": True}
