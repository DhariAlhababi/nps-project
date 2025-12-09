from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_parks():
    response = client.get("/parks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_alerts():
    response = client.get("/alerts/search", params={"keyword": "fire"})
    assert response.status_code == 200

def test_analytics():
    response = client.get("/analytics/top-alert-parks")
    assert response.status_code == 200
