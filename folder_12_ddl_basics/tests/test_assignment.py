import sqlite3
import os
import pytest

def test_assignment_sql():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(current_dir, '..', 'assignment.sql')
    
    with open(sql_file, 'r') as f:
        sql_script = f.read()
        
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    statements = sql_script.split(';')
    
    books_created = False
    books_genre_added = False
    members_created = False
    
    try:
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt:
                continue
            cursor.execute(stmt)
            
            if 'CREATE TABLE books' in stmt.upper() or 'CREATE TABLE "books"' in stmt.upper():
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
                if cursor.fetchone():
                    books_created = True
                    
            if 'CREATE TABLE members' in stmt.upper() or 'CREATE TABLE "members"' in stmt.upper():
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='members'")
                if cursor.fetchone():
                    members_created = True
                    
            if 'ALTER TABLE books' in stmt.upper() and 'genre' in stmt.lower():
                cursor.execute("PRAGMA table_info(books)")
                columns = [info[1] for info in cursor.fetchall()]
                if 'genre' in columns:
                    books_genre_added = True

        assert books_created, "Table 'books' was not created."
        assert members_created, "Table 'members' was not created."
        assert books_genre_added, "Column 'genre' was not added to 'books'."
        
        # Verify members was dropped
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='members'")
        assert cursor.fetchone() is None, "Table 'members' should have been dropped."
            
    except sqlite3.Error as e:
        pytest.fail(f"SQL execution failed: {e}")
    finally:
        conn.close()
