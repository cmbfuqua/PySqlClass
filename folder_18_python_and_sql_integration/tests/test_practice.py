import sqlite3
import pytest
import tempfile
import os
from ..practice import get_active_users

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp()
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, is_active INTEGER)")
    cursor.execute("INSERT INTO users (username, is_active) VALUES ('alice', 1), ('bob', 0), ('charlie', 1)")
    conn.commit()
    conn.close()
    
    yield path
    
    os.close(fd)
    os.remove(path)

def test_get_active_users(temp_db):
    result = get_active_users(temp_db)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == {'id': 1, 'username': 'alice'}
    assert result[1] == {'id': 3, 'username': 'charlie'}
