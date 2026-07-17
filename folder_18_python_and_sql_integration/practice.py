import sqlite3
# TODO: Fetch users using row_factory
def get_users(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    rows = cursor.execute('SELECT name FROM users LIMIT 1').fetchall()
    conn.close()
    return [row['name'] for row in rows]
