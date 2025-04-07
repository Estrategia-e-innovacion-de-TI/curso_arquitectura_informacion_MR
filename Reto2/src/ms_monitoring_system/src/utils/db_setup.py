from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------- DB SETUP ----------------
DATABASE_URL = "sqlite:///./db/tracking_monitor.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)