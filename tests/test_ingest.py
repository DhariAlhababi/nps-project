from backend.app.services.nps_fetcher import upsert_parks

def test_parks_ingestion():
    try:
        upsert_parks()
    except Exception:
        assert False
