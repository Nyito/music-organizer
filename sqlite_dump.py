import sqlite3

conn = sqlite3.connect("spotify_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    display_name TEXT,
    country TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tracks (
    id TEXT PRIMARY KEY,
    name TEXT,
    artist TEXT,
    album TEXT,
    popularity INTEGER,
    duration_ms INTEGER
);
""")

conn.commit()
print("Database and tables created!")
conn.close()