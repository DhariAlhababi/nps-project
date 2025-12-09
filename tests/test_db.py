from backend.app.database import engine
from sqlmodel import inspect

def test_tables_exist():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "park" in tables
    assert "campground" in tables
    assert "alert" in tables
