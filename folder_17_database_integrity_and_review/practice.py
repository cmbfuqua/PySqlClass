import sqlite3
# TODO: Write a function to check if users table exists
def check_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
