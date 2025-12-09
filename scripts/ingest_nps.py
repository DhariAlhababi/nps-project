from backend.app.database import create_db_and_tables
from backend.app.services.nps_fetcher import upsert_parks, upsert_campgrounds, upsert_alerts

if __name__ == "__main__":
    create_db_and_tables()
    upsert_parks()
    upsert_campgrounds()
    upsert_alerts()
    print("Ingestion completed!")
