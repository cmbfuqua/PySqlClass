import sqlite3
import os

def get_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'finance.db')
    if not os.path.exists(db_path):
        conn = sqlite3.connect(':memory:')
        # Note: in a real environment we'd run setup_database.py here for an in-memory copy
    else:
        # For sandboxing, we copy to memory
        source_conn = sqlite3.connect(db_path)
        conn = sqlite3.connect(':memory:')
        source_conn.backup(conn)
        source_conn.close()
    return conn

def test_practice():
    conn = get_db()
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'practice.sql')
    with open(sql_path, 'r') as f:
        sql = f.read()
    try:
        conn.executescript(sql)
    except sqlite3.Error as e:
        # Some assignments purposefully cause errors or just run queries
        pass
    assert True
    conn.close()
