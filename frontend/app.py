import streamlit as st
import pandas as pd
import requests
import plotly.express as px


API = "http://localhost:8000"
st.set_page_config(page_title="National Parks Explorer", layout="wide")

st.title("🏞️ National Parks Information System")


# ----------------------------------------------------------------------
#                             LOAD PARKS
# ----------------------------------------------------------------------
st.header("📌 All National Parks")
parks = requests.get(f"{API}/parks").json()
df_parks = pd.DataFrame(parks)

st.dataframe(df_parks)

# Map View
if "latitude" in df_parks and "longitude" in df_parks:
    st.subheader("🗺️ Park Locations Map")
    st.map(df_parks[["latitude", "longitude"]].dropna())


# ----------------------------------------------------------------------
#                             ALERT SEARCH
# ----------------------------------------------------------------------
st.header("🚨 Search Alerts")
keyword = st.text_input("Enter search keyword (e.g., fire, closure, weather)")
if keyword:
    alerts = requests.get(f"{API}/alerts/search",
                          params={"keyword": keyword}).json()
    st.dataframe(pd.DataFrame(alerts))


# ----------------------------------------------------------------------
#                         CAMPGROUND SEARCH
# ----------------------------------------------------------------------
st.header("⛺ Search Campgrounds")
min_sites = st.number_input("Minimum Campsite Capacity", min_value=0)
if min_sites > 0:
    campgrounds = requests.get(
        f"{API}/campgrounds/search",
        params={"min_sites": min_sites}
    ).json()
    st.dataframe(pd.DataFrame(campgrounds))


# ----------------------------------------------------------------------
#                             ANALYTICS
# ----------------------------------------------------------------------
st.header("📊 Analytics & Insights")

# ---- 1. Top Alert Parks ----
st.subheader("🔥 Top 10 Parks with Most Alerts")
top_alerts = requests.get(f"{API}/analytics/top-alert-parks").json()
df_top_alerts = pd.DataFrame(top_alerts)
st.dataframe(df_top_alerts)

if not df_top_alerts.empty:
    st.plotly_chart(
        px.bar(df_top_alerts,
               x="name",
               y="alert_count",
               title="Top 10 Parks with Most Alerts")
    )


# ---- 2. Total Campground Capacity by State ----
st.subheader("⛺ Total Campground Capacity by State")
caps = requests.get(f"{API}/analytics/campground-capacity").json()
df_caps = pd.DataFrame(caps)
st.dataframe(df_caps)

if not df_caps.empty:
    st.plotly_chart(
        px.bar(df_caps,
               x="states",
               y="total_capacity",
               title="Total Campground Capacity by State")
    )


# ---- 3. Parks with Campgrounds >200 Sites ----
st.subheader("🏕️ Parks with Campgrounds Larger than 200 Sites")
large = requests.get(f"{API}/analytics/parks-large-campgrounds").json()
st.dataframe(pd.DataFrame(large))


# ---- 4. Recent Closures ----
st.subheader("🚧 Parks with >5 Closures in the Last Year")
recent_close = requests.get(f"{API}/analytics/recent-closure-parks").json()
st.dataframe(pd.DataFrame(recent_close))


# ---- 5. Parks per State ----
st.subheader("📍 Number of Parks per State")
pps = requests.get(f"{API}/analytics/parks-per-state").json()
st.dataframe(pd.DataFrame(pps))


# ---- 6. Average Campsites ----
st.subheader("📐 Average Number of Campsites")
avg = requests.get(f"{API}/analytics/avg-campsites").json()
st.dataframe(pd.DataFrame(avg))


# ---- 7. Alerts per Category ----
st.subheader("📢 Alerts by Category")
cat = requests.get(f"{API}/analytics/alerts-per-category").json()
st.dataframe(pd.DataFrame(cat))

if cat:
    df_cat = pd.DataFrame(cat)
    st.plotly_chart(px.pie(df_cat, names="category", values="count",
                           title="Alert Category Distribution"))


# ---- 8. No-Reservation Campgrounds ----
st.subheader("🚫 Campgrounds Without Reservation URLs")
no_res = requests.get(f"{API}/analytics/no-reservation-campgrounds").json()
st.dataframe(pd.DataFrame(no_res))


# ---- 9. Missing Coordinates ----
st.subheader("❗ Parks Missing Coordinates")
missing = requests.get(f"{API}/analytics/missing-coordinates").json()
st.dataframe(pd.DataFrame(missing))


# ---- 10. Campgrounds by State ----
st.subheader("🔎 Search Campgrounds by State")

state_query = st.text_input("Enter state abbreviation(s). Example: CA or CA,TX,FL")

if state_query:
    # Normalize input → split into list
    states = [s.strip().upper() for s in state_query.replace(" ", "").split(",")]

    all_results = []

    for s in states:
        response = requests.get(
            f"{API}/analytics/campgrounds-by-state",
            params={"state": s}
        )

        if response.status_code == 200:
            try:
                data = response.json()
                all_results.extend(data)
            except:
                st.error(f"Invalid JSON from backend for {s}")
        else:
            st.error(f"Server error for state {s}: {response.text}")

    if all_results:
        st.dataframe(pd.DataFrame(all_results))
    else:
        st.warning("No campgrounds found for the given states.")

