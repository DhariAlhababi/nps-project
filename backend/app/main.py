from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, text, Session
from backend.app.database import create_db_and_tables, get_session
from backend.app.models import Park, Campground, Alert
from fastapi import Depends

app = FastAPI(title="NPS Info API")

# ---------------- CORS --------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nps-explorer-url.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STARTUP --------------
@app.on_event("startup")
def start_app():
    create_db_and_tables()


# ---------------- PARK ROUTES ----------------
@app.get("/parks")
def get_parks(q: str = None):
    with get_session() as session:
        stmt = select(Park)
        if q:
            stmt = stmt.where(Park.name.ilike(f"%{q}%"))
        return session.exec(stmt).all()


@app.get("/parks/{park_id}")
def get_park(park_id: str):
    with get_session() as session:
        park = session.get(Park, park_id)
        if not park:
            raise HTTPException(status_code=404, detail="Park not found")
        return park


# ---------------- ALERT SEARCH ----------------

@app.get("/parks/{park_id}/alerts")
def get_alerts_by_park(park_id: str):
    with get_session() as session:
        stmt = select(Alert).where(Alert.park_id == park_id)
        return session.exec(stmt).all()


@app.get("/alerts/search")
def search_alerts(keyword: str = Query(...)):
    with get_session() as session:
        stmt = select(Alert).where(
            (Alert.title.ilike(f"%{keyword}%")) |
            (Alert.description.ilike(f"%{keyword}%"))
        )
        return session.exec(stmt).all()

@app.get("/campgrounds")
def get_all_campgrounds():
    with get_session() as session:
        return session.exec(select(Campground)).all()
    
@app.get("/parks/{park_id}/campgrounds")
def get_campgrounds_by_park(park_id: str):
    with get_session() as session:
        stmt = select(Campground).where(Campground.park_id == park_id)
        return session.exec(stmt).all()

# ---------------- CAMPGROUND SEARCH ----------------
@app.get("/campgrounds/search")
def search_campgrounds(min_sites: int = 0):
    with get_session() as session:
        stmt = select(Campground).where(Campground.total_sites >= min_sites)
        return session.exec(stmt).all()


# ---------------- ANALYTICS QUERIES ----------------

def rows_to_dict(result):
    return [dict(r._mapping) for r in result]

@app.get("/analytics/parks-large-campgrounds")
def parks_large_campgrounds():
    with get_session() as session:
        sql = text("""SELECT DISTINCT p.name, c.total_sites
                       FROM park p
                       JOIN campground c ON p.park_id = c.park_id
                       WHERE c.total_sites > 200""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/top-alert-parks")
def top_alert_parks():
    with get_session() as session:
        sql = text("""SELECT p.name, COUNT(a.alert_id) AS alert_count
                       FROM park p
                       JOIN alert a ON p.park_id = a.park_id
                       GROUP BY p.name
                       ORDER BY alert_count DESC
                       LIMIT 10""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/campground-capacity")
def campground_capacity():
    with get_session() as session:
        sql = text("""SELECT p.states, SUM(c.total_sites) AS total_capacity
                       FROM park p
                       JOIN campground c ON p.park_id = c.park_id
                       GROUP BY p.states""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/recent-closure-parks")
def recent_closure_parks():
    with get_session() as session:
        sql = text("""SELECT p.name, COUNT(a.alert_id) AS closure_count
                       FROM park p
                       JOIN alert a ON p.park_id = a.park_id
                       WHERE a.category = 'Closure'
                       AND date(a.date_created) >= date('now', '-1 year')
                       GROUP BY p.name
                       HAVING closure_count > 5""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/parks-per-state")
def parks_per_state():
    with get_session() as session:
        sql = text("""SELECT states, COUNT(*) AS park_count
                       FROM park GROUP BY states""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/avg-campsites")
def avg_campsites():
    with get_session() as session:
        sql = text("""SELECT AVG(total_sites) AS avg_sites FROM campground""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/alerts-per-category")
def alerts_per_category():
    with get_session() as session:
        sql = text("""SELECT category, COUNT(*) AS count
                       FROM alert GROUP BY category""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/no-reservation-campgrounds")
def no_reservation_campgrounds():
    with get_session() as session:
        sql = text("""SELECT name, park_id
                       FROM campground
                       WHERE reservation_url IS NULL OR reservation_url = ''""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/missing-coordinates")
def missing_coordinates():
    with get_session() as session:
        sql = text("""SELECT park_id, name
                       FROM park
                       WHERE latitude IS NULL OR longitude IS NULL""")
        return rows_to_dict(session.exec(sql).all())

@app.get("/analytics/campgrounds-by-state")
def campgrounds_by_state(state: str, session: Session = Depends(get_session)):
    sql = text("""
        SELECT 
            c.name AS campgroundName,
            p.states AS state,
            COUNT(*) AS occurrences
        FROM campground c
        JOIN park p ON c.park_id = p.park_id
        WHERE p.states LIKE :state
        GROUP BY c.name, p.states
    """)

    rows = session.execute(sql, {"state": f"%{state}%"}).fetchall()

    return [
        {
            "campgroundName": r.campgroundName,
            "state": r.state,
            "occurrences": r.occurrences
        }
        for r in rows
    ]