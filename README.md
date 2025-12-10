# National Parks Information System  
A full-stack data application that collects, stores, analyzes, and visualizes data from the U.S. National Park Service (NPS).  
Built with **FastAPI**, **SQLModel**, **PostgreSQL**, and **Streamlit**.

---

## 🚀 Project Overview
This project automatically fetches real data from the **NPS Public API**, stores it in a database, and exposes rich API endpoints for parks, campgrounds, alerts, and analytical insights.  
A user-friendly **Streamlit dashboard** presents interactive maps, tables, and search features.

---

## 📂 Technologies Used
### **Backend**
- FastAPI  
- SQLModel  
- PostgreSQL  
- Uvicorn  
- NPS Public API  

### **Frontend**
- Streamlit  
- Pandas  
- Requests  

### **Deployment**
- Render (Backend API)  
- Streamlit Cloud (Frontend UI)

---

## 📦 Features

### ✔ **Data Ingestion**
Automatically fetches and stores:
- National Parks  
- Campgrounds  
- Alerts / Warnings  

### ✔ **REST API Endpoints**
Key endpoints include:
- `/parks`
- `/parks/{park_id}`
- `/parks/{park_id}/campgrounds`
- `/parks/{park_id}/alerts`
- `/campgrounds/search`
- `/alerts/search`

### ✔ **Advanced Analytics Endpoints**
Includes SQL-powered insights such as:
- Parks with large campgrounds  
- Total campground capacity by state  
- Parks with highest alert count  
- Alerts per category  
- Average campsites  
- Recently closed parks  
- Campgrounds without reservations  

### ✔ **Interactive Streamlit Dashboard**
- View all parks  
- Explore parks on a live map  
- Search alerts and campgrounds  
- Visualize analytics  
- Clean UI for users  

---

## 🗄 Database Schema

### **Park Table**
- park_id  
- name  
- states  
- latitude  
- longitude  
- description  
- url  

### **Campground Table**
- campground_id  
- park_id (FK)  
- name  
- total_sites  
- reservation_url  

### **Alert Table**
- alert_id  
- park_id (FK)  
- title  
- category  
- description  
- date_created  

---

## ⚙️ How the System Works

1. **Data Fetch**
   - Python script calls NPS API and loads data.

2. **Database Processing**
   - Cleans and normalizes data.
   - Inserts/updates tables.

3. **API Service**
   - FastAPI exposes endpoints for parks, alerts, campgrounds, and analytics.

4. **Frontend Visualization**
   - Streamlit fetches from FastAPI.
   - Displays map, tables, and search UI.

---

## ▶️ Running the System Locally

### **1. Start Backend**
uvicorn backend.app.main:app --reload --port 8000

### **2. Start Frontend**
streamlit run frontend/app.py

### **3. Access UI**
http://localhost:8501

---

## 🧪 Testing
The project includes automated tests.  
Run tests with:
pytest -q

---

## 🌐 Deployment Architecture


┌────────────────┐ ┌───────────────────────────┐
│ Streamlit Cloud │ ---> │ Render FastAPI Backend API │
└────────────────┘ └───────────────────────────┘
│
▼
PostgreSQL (Render)


Backend → connects to hosted PostgreSQL  
Frontend → calls backend API endpoints

---

## 👤 Author
**Dhari Alhabib**  
National Parks Information System

---

## ⭐ Project Status
✔ Backend Complete  
✔ Database Integrated  
✔ Full Analytics Implemented  
✔ Frontend Dashboard Completed  
✔ Fully Tested  
✔ Deployment Ready  

