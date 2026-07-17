import sqlite3
import pytest
from ..assignment import transfer_funds

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance REAL)")
    cursor.execute("INSERT INTO accounts (id, balance) VALUES (1, 100.0), (2, 50.0)")
    conn.commit()
    yield conn
    conn.close()

def test_transfer_funds_success(db_connection):
    result = transfer_funds(db_connection, 1, 2, 25.0)
    assert result is True
    
    cursor = db_connection.cursor()
    cursor.execute("SELECT balance FROM accounts ORDER BY id")
    balances = cursor.fetchall()
    assert balances[0][0] == 75.0
    assert balances[1][0] == 75.0

def test_transfer_funds_negative_amount(db_connection):
    result = transfer_funds(db_connection, 1, 2, -10.0)
    assert result is False
    
    cursor = db_connection.cursor()
    cursor.execute("SELECT balance FROM accounts ORDER BY id")
    balances = cursor.fetchall()
    assert balances[0][0] == 100.0
    assert balances[1][0] == 50.0

def test_transfer_funds_insufficient_funds(db_connection):
    result = transfer_funds(db_connection, 1, 2, 150.0)
    assert result is False
    
    cursor = db_connection.cursor()
    cursor.execute("SELECT balance FROM accounts ORDER BY id")
    balances = cursor.fetchall()
    assert balances[0][0] == 100.0
    assert balances[1][0] == 50.0
