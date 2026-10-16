"""
Database setup and models for Usha Sree's Portfolio Backend
Using SQLite with SQLAlchemy ORM
"""

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Path for the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "portfolio.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ContactMessage(Base):
    """Stores inquiries sent by recruiters & visitors"""
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class VisitorLog(Base):
    """Tracks visitor visits for analytics"""
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_hash = Column(String(64), nullable=True)
    user_agent = Column(String(255), nullable=True)
    visited_at = Column(DateTime, default=datetime.utcnow)


class SiteStat(Base):
    """Aggregate statistics like total views"""
    __tablename__ = "site_stats"

    id = Column(Integer, primary_key=True, index=True)
    total_views = Column(Integer, default=0)


def init_db():
    """Create tables and initialize stats if empty"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        stat = db.query(SiteStat).first()
        if not stat:
            # Seed starting count for realistic portfolio presentation
            db.add(SiteStat(total_views=128))
            db.commit()
    finally:
        db.close()


def get_db():
    """FastAPI Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
