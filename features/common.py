import os
import sqlite3

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "movies.db",
)

def connect():
    if not os.path.exists(DB_PATH):
        raise sqlite3.OperationalError(
            f"database not found at {DB_PATH}; run `python scripts/seed_db.py` first"
        )
    return sqlite3.connect(DB_PATH)


def redact(error, secret):
    #Return str(error) with the API key masked.
    text = str(error)
    if secret:
        text = text.replace(secret, "***")
    return text
