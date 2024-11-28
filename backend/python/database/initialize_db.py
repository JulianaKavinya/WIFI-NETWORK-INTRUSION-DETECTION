# initialize_db.py
from sqlalchemy import create_engine
from .models import Base
from backend.python.config import DATABASE_URL
def initialize_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
