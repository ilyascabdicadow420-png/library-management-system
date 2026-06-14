"""Database connection and setup utilities for the Library Management System."""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "library.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection(db_path=DEFAULT_DB_PATH):
    """Return a SQLite connection with foreign keys enabled."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path=DEFAULT_DB_PATH):
    """Create all required tables if they do not already exist."""
    connection = get_connection(db_path)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())
    connection.commit()
    return connection
