from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)
def test_alert_search():
    r = client.get("/alerts/search?keyword=fire")
    assert r.status_code == 200
