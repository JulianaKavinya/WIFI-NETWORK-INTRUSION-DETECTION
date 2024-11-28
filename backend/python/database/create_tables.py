# database/create_tables.py
from database.db import engine
from database.models import Base

# Create tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
