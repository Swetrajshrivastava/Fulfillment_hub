
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "fulfillment.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def query(sql, params=()):
    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()

def execute(sql, params=()):
    with get_connection() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
