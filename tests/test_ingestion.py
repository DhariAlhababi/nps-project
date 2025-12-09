from scripts.ingest_nps import upsert_parks

def test_ingest_runs():
    upsert_parks()
    assert True  # No errors = pass
