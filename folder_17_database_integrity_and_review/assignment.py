"""
Database Integrity & Transactions - Assignment

Problem: Bank Transfer
You are tasked with writing a function that performs a bank transfer between two accounts using SQLite.

Function Signature:
def transfer_funds(conn: sqlite3.Connection, from_account: int, to_account: int, amount: float) -> bool:

Requirements:
1. The database has an 'accounts' table with 'id' and 'balance'.
2. The function must deduct `amount` from `from_account` and add `amount` to `to_account`.
3. The transaction must fail and be rolled back if `amount` is negative or if `from_account` does not have enough balance.
4. If successful, commit the transaction and return True. If it fails, rollback and return False.
"""
import sqlite3

def transfer_funds(conn: sqlite3.Connection, from_account: int, to_account: int, amount: float) -> bool:
    pass
