# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL (example for SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./network_monitor.db")