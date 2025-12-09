import os
import httpx
from dotenv import load_dotenv
from sqlmodel import Session
from backend.app.database import get_session
from backend.app.models import Park, Campground, Alert

load_dotenv()
API_KEY = os.getenv("NPS_API_KEY")
BASE = "https://developer.nps.gov/api/v1"

def fetch(endpoint, params=None):
    params = params or {}
    params["api_key"] = API_KEY
    r = httpx.get(f"{BASE}/{endpoint}", params=params)
    return r.json()

def upsert_parks():
    data = fetch("parks", {"limit": 500})
    parks = data.get("data", [])

    with get_session() as session:
        for p in parks:
            park_id = p.get("parkCode")
            latlong = p.get("latLong", "")

            # Simple parsing
            lat, lon = None, None
            if latlong and "lat:" in latlong:
                try:
                    parts = latlong.replace("lat:", "").replace("long:", "").split(",")
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                except:
                    pass

            park = Park(
                park_id=park_id,
                name=p.get("fullName"),
                states=p.get("states"),
                latitude=lat,
                longitude=lon,
                description=p.get("description"),
                url=p.get("url")
            )

            session.merge(park)
        session.commit()

    print("Parks updated successfully!")

def upsert_campgrounds():
    data = fetch("campgrounds", {"limit": 500})
    campgrounds = data.get("data", [])

    with get_session() as session:
        for c in campgrounds:
            campground_id = c.get("id")  # depends on API field
            campground = Campground(
                campground_id=campground_id,
                park_id=c.get("parkCode"),
                name=c.get("name"),
                total_sites=int(c.get("campsites", {}).get("totalSites", 0)),
                reservation_url=c.get("reservationUrl")
            )
            session.merge(campground)
        session.commit()

    print("Campgrounds updated successfully!")

def upsert_alerts():
    data = fetch("alerts", {"limit": 500})
    alerts = data.get("data", [])

    with get_session() as session:
        for a in alerts:
            alert_id = a.get("id")
            alert = Alert(
                alert_id=alert_id,
                park_id=a.get("parkCode"),
                title=a.get("title"),
                category=a.get("category"),
                description=a.get("description"),
                date_created=a.get("dateCreated")
            )
            session.merge(alert)
        session.commit()
    print("Alerts updated successfully!")


