from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.python.config import DATABASE_URL
from .models import Base

# Setup engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite-specific
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database (create tables)
def init_db():
    """Create tables in the database."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
