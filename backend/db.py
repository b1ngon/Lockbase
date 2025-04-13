import MySQLdb
import os
from dotenv import load_dotenv
from pathlib import Path

# Resolve the .env file path safely
env_path = Path(__file__).resolve().parent.parent / "config" / "settings.env"
load_dotenv(dotenv_path=env_path)

def get_db_connection():
    return MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        passwd=os.getenv("MYSQL_PASSWORD"),  # ✅ Use the correct env variable
        db=os.getenv("MYSQL_DB")
    )
