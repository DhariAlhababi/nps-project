from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_parks():
    response = client.get("/parks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_park():
    # acad = Acadia National Park (example)
    response = client.get("/parks/acad")
    # 200 or 404 both are valid depending on data
    assert response.status_code in (200, 404)

def test_invalid_route():
    response = client.get("/invalid")
    assert response.status_code == 404
