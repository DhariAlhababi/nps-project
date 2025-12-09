from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_campgrounds():
    r = client.get("/campgrounds")
    assert r.status_code == 200
