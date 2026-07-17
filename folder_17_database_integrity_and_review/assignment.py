import sqlite3
def verify_foreign_keys(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_key_check;')
    violations = cursor.fetchall()
    conn.close()
    return len(violations) == 0
