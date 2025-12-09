from backend.app.database import create_db_and_tables

def test_db_tables():
    try:
        create_db_and_tables()
    except Exception:
        assert False
