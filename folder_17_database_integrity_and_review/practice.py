"""
Database Integrity & Transactions - Practice

Examples:
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
try:
    cursor.execute("BEGIN TRANSACTION;")
    # ... operations
    conn.commit()
except:
    conn.rollback()
"""
import sqlite3

def safe_update_product_price(conn: sqlite3.Connection, product_id: int, new_price: float) -> bool:
    """
    Update a product's price within a transaction. 
    If the new_price is negative, raise a ValueError and ensure no changes are committed.
    Returns True if successful, False if an error occurred.
    
    Starter code is incomplete.
    """
    cursor = conn.cursor()
    
    # TODO: Begin transaction
    # TODO: Check if new_price < 0, raise ValueError if it is
    # TODO: Execute update on 'products' table setting 'price' where 'id' = product_id
    # TODO: Commit transaction and return True
    # TODO: Handle exceptions, rollback, and return False
    pass
