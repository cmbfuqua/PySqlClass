# Database Integrity and Review

## Overview
Database integrity refers to the overarching accuracy, consistency, and reliability of data stored within a relational database system throughout its entire lifecycle. Maintaining data integrity is a non-negotiable requirement for any system intended for production use. It encompasses various techniques, constraints, and operational paradigms that act together to ensure data is logically sound, conforms to specific rules, and remains intact even during unforeseen hardware or software failures.

At the core of maintaining database integrity during operational transactions is the concept of a **Transaction**, which follows the well-known **ACID properties**:
- **Atomicity**: This principle dictates that a transaction is treated as a single, indivisible logical unit of work. All the operations within the transaction must succeed completely, or none of them do. There is no such thing as a "partial success." If any individual step fails (e.g., due to a constraint violation or a system crash), the entire transaction is aborted, and the database is rolled back to the state it was in before the transaction began.
- **Consistency**: The database must transition smoothly from one valid state to another. A valid state is one where all the defined rules, constraints (like foreign keys, unique constraints, and check constraints), cascades, and triggers are satisfied. Consistency ensures that an atomic transaction doesn't violate the foundational schema or rules set by the database administrator.
- **Isolation**: In any moderately busy database, multiple transactions will be happening simultaneously. Isolation guarantees that these concurrent transactions do not interfere with one another. The intermediate states of an ongoing transaction are completely invisible to other concurrent transactions. Depending on the chosen isolation level (Read Uncommitted, Read Committed, Repeatable Read, or Serializable), the database manages locks or employs multi-version concurrency control (MVCC) to ensure operations appear as though they were executed sequentially.
- **Durability**: Once a transaction has been successfully committed, the changes made to the data are permanently recorded and will survive any subsequent system failures, power outages, or crashes. This is typically achieved by writing transaction logs to non-volatile storage before confirming the commit to the application.

In SQL, and particularly when interfacing via Python's `sqlite3` module, transactions are manually or automatically controlled using `BEGIN TRANSACTION`, `COMMIT`, and `ROLLBACK` statements.

## Why it's important
Without transaction management and robust integrity checks, databases are highly susceptible to corruption, data anomalies, and illogical states. To understand the gravity of this, imagine a scenario where you are transferring $500 from your savings account to your checking account. This operation involves at least two separate SQL updates:
1. Deducting $500 from the savings account balance.
2. Adding $500 to the checking account balance.

If these two updates are not bound within an atomic transaction, what happens if the server crashes exactly after step 1 but before step 2? Your savings account would be debited, but your checking account would not be credited. The $500 effectively vanishes into thin air. From the perspective of a banking system, this is a catastrophic failure.

Deep diving further, integrity constraints such as Primary Keys, Foreign Keys, and CHECK constraints act as the first line of defense against dirty data. A foreign key constraint, for instance, prevents "orphan records" by ensuring that a record in a child table cannot exist without a corresponding valid record in the parent table. If an application attempts to insert an order for a customer ID that doesn't exist, the database itself outright rejects the operation, shielding the system from application-level bugs. The data layer acts as the absolute ultimate source of truth, and its integrity mechanisms protect it from application-layer errors.

## Common Pitfalls
1. **Long-Running Transactions**: Keeping a transaction open for a prolonged period while executing complex business logic or waiting for external API calls can lock database tables, leading to severe performance bottlenecks and deadlocks for other users. Always keep transactions as short as possible. Fetch necessary data, do application-level logic outside the transaction, and open a new brief transaction to apply changes.
2. **Silent Failures and Uncaught Exceptions**: If you execute a series of statements inside a try block but fail to catch specific database exceptions properly, the application might think the transaction succeeded even if it didn't, or it might fail to explicitly `ROLLBACK`, leaving the connection in an unpredictable state and leaving locks engaged.
3. **Deadlocks**: This occurs when two separate concurrent transactions each hold a lock on a resource that the other transaction needs to proceed. Both end up waiting indefinitely. Proper application design (e.g., always acquiring locks in the same consistent order across all transactions) and database tuning are required to resolve and prevent deadlocks.
4. **Ignoring Autocommit**: Different database drivers have different default behaviors. Some Python drivers default to `autocommit=True`, meaning every single statement is immediately committed, nullifying your attempts to manually group them into a transaction unless you explicitly start one.

## Advanced Edge Cases
- **Nested Transactions and Savepoints**: Some complex applications require partial rollbacks within a larger transaction. For example, you might be processing a batch of 100 items. If item 50 fails, you might want to roll back only the work done for item 50, log the error, and continue processing the rest, rather than aborting the entire batch. SQL provides `SAVEPOINT` and `ROLLBACK TO SAVEPOINT` for this exact advanced scenario.
- **Isolation Level Anomalies**: Depending on your isolation level, you might encounter phenomena like "Dirty Reads" (reading uncommitted data), "Non-Repeatable Reads" (a row changes its value when read twice within the same transaction), or "Phantom Reads" (new rows appear that match a query criteria during the same transaction). Understanding how to set the appropriate isolation level for a specific transaction is a key advanced database skill. Serializability avoids all these but sacrifices concurrency throughput.

## Examples

### Example 1: A Secure Bank Transfer
This example demonstrates a complete, atomic bank transfer with comprehensive error handling in Python using `sqlite3`.

```python
import sqlite3

def secure_transfer(db_path, sender_id, receiver_id, amount):
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Explicitly start the transaction
        cursor.execute("BEGIN TRANSACTION;")
        
        # Check sender's current balance to prevent overdraft
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (sender_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Sender account not found.")
            
        current_balance = row[0]
        if current_balance < amount:
            raise ValueError("Insufficient funds for transfer.")
        
        # Deduct from sender
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, sender_id))
        
        # Add to receiver
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, receiver_id))
        
        # If everything succeeds, commit the transaction
        conn.commit()
        print("Transfer completed successfully.")
        
    except sqlite3.Error as e:
        # A database-level error occurred
        conn.rollback()
        print(f"Database error during transfer: {e}")
    except ValueError as ve:
        # A business logic error occurred
        conn.rollback()
        print(f"Transfer failed: {ve}")
    finally:
        # Always close the connection
        conn.close()
```

### Example 2: Using Savepoints for Partial Rollbacks
This advanced example shows how to use `SAVEPOINT` to handle errors on an item-by-item basis without aborting the entire transaction.

```python
import sqlite3

def process_batch(db_path, batch_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN TRANSACTION;")
        
        for index, item in enumerate(batch_data):
            # Create a savepoint for this specific item
            savepoint_name = f"sp_item_{index}"
            cursor.execute(f"SAVEPOINT {savepoint_name};")
            
            try:
                # Attempt complex, risky insertion
                cursor.execute("INSERT INTO audit_log (data) VALUES (?)", (item['data'],))
                # Release savepoint (optional, but good practice to free resources)
                cursor.execute(f"RELEASE SAVEPOINT {savepoint_name};")
            except sqlite3.IntegrityError:
                # If this specific item fails, rollback just this item
                cursor.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name};")
                print(f"Item {index} failed and was rolled back, continuing with others.")
        
        # Finally, commit whatever succeeded in the batch
        conn.commit()
        
    except sqlite3.Error as e:
        # If something goes catastrophically wrong with the main transaction
        conn.rollback()
        print(f"Batch processing failed entirely: {e}")
    finally:
        conn.close()
```
