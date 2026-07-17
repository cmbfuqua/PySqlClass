"""
Python and SQL Integration - Practice

Examples:
To execute a parameterized query safely and avoid SQL injection:
cursor.execute("SELECT * FROM users WHERE age > ?", (min_age,))
rows = cursor.fetchall()
"""
import sqlite3

def get_active_users(db_path: str) -> list:
    """
    Connects to the database at `db_path` and retrieves all users
    where the `is_active` column is 1 (True).
    
    The 'users' table has columns: 'id', 'username', 'is_active'.
    
    Returns a list of dictionaries, e.g.:
    [{'id': 1, 'username': 'alice'}, {'id': 2, 'username': 'bob'}]
    
    Starter code is incomplete.
    """
    # TODO: Connect to the database
    # TODO: Set conn.row_factory to sqlite3.Row for dict conversion
    # TODO: Execute query to select id, username from users where is_active = 1
    # TODO: Fetch all rows and convert them to dictionaries
    # TODO: Close connection and return the list
    pass
