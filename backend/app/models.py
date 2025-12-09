from typing import Optional
from sqlmodel import SQLModel, Field



class Park(SQLModel, table=True):
    park_id: str = Field(primary_key=True)
    name: str
    states: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    url: Optional[str] = None

class Campground(SQLModel, table=True):
    campground_id: str = Field(primary_key=True)
    park_id: str = Field(foreign_key="park.park_id")
    name: str
    total_sites: Optional[int] = None
    reservation_url: Optional[str] = None

class Alert(SQLModel, table=True):
    alert_id: str = Field(primary_key=True)
    park_id: str = Field(foreign_key="park.park_id")
    title: str
    category: Optional[str] = None
    description: Optional[str] = None
    date_created: Optional[str] = None
