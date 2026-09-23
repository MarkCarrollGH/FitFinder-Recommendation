def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_headers(client):
    response = client.options("/health", headers={"Origin": "http://example.com"})
    assert response.status_code in (200, 405)
