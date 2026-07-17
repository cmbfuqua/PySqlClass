import sqlite3
import os
import pytest

def test_practice():
    # Setup in-memory DB
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create tables and insert dummy data
    cursor.execute("""
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product_category TEXT,
            revenue REAL,
            region TEXT
        )
    """)
    cursor.executemany("""
        INSERT INTO sales (product_category, revenue, region) VALUES (?, ?, ?)
    """, [
        ('Electronics', 100.0, 'North'),
        ('Electronics', 150.0, 'North'),
        ('Clothing', 50.0, 'South'),
        ('Clothing', 75.0, 'North'),
        ('Electronics', 200.0, 'South')
    ])
    
    # Read the practice file
    practice_file = os.path.join(os.path.dirname(__file__), '..', 'practice.sql')
    with open(practice_file, 'r') as f:
        sql_script = f.read()
        
    try:
        cursor.executescript(sql_script)
    except sqlite3.OperationalError:
        pytest.fail("SQL script failed to execute. Did you fill in all the blanks?")
        
    # Check category_revenue view
    try:
        cursor.execute("SELECT product_category, total_revenue FROM category_revenue ORDER BY product_category")
        results = cursor.fetchall()
        assert results == [('Clothing', 125.0), ('Electronics', 450.0)], "category_revenue results are incorrect."
    except sqlite3.OperationalError:
        pytest.fail("View category_revenue does not exist or has incorrect columns.")

    # Check region_stats view
    try:
        cursor.execute("SELECT region, avg_revenue, min_revenue, max_revenue FROM region_stats ORDER BY region")
        results = cursor.fetchall()
        expected = [
            ('North', 108.33333333333333, 75.0, 150.0),
            ('South', 125.0, 50.0, 200.0)
        ]
        assert results == expected, "region_stats results are incorrect."
    except sqlite3.OperationalError:
        pytest.fail("View region_stats does not exist or has incorrect columns.")
