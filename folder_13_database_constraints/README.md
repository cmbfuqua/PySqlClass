# Database Constraints

## Overview

In the realm of relational database management systems (RDBMS), data integrity is paramount. Database constraints are a fundamental mechanism used to ensure the accuracy, reliability, and consistency of the data stored within a database. At their core, constraints are strict rules applied to columns (or entire tables) that restrict the types of data, values, or relationships that can be inserted, updated, or deleted. 

When you design a database schema, you are essentially defining a contract for your data. Constraints are the enforcers of this contract. If any database transaction attempts to violate a constraint, the database engine will reject the operation and throw an error, preventing invalid data from entering the system. This proactive approach to data validation happens at the lowest level of the data storage layer, which is far more secure and reliable than relying solely on application-level validation.

There are several standard constraints defined in SQL:
- `NOT NULL`: Ensures a column cannot contain a NULL (empty) value.
- `UNIQUE`: Guarantees that all values in a column (or a combination of columns) are entirely unique across the table.
- `PRIMARY KEY`: A specific combination of `NOT NULL` and `UNIQUE` that uniquely identifies every single row in a table.
- `FOREIGN KEY`: Ensures referential integrity between two tables (discussed more in folder 14).
- `CHECK`: Validates that data in a column meets a specific boolean condition.
- `DEFAULT`: Automatically assigns a specified default value if no explicit value is provided during an insert operation.

## Why it's important (Deep Dive)

The importance of database constraints cannot be overstated. Consider what happens when constraints are not used. 

**1. Data Corruption and Anomalies**
Without constraints, an application bug could easily insert a negative value for an employee's salary, an empty string for a critical email address, or a duplicate username. Over time, this leads to a phenomenon known as data rot or data corruption. Bad data compounds, making reports inaccurate, analytics misleading, and causing downstream application failures. Constraints act as a final, impenetrable wall that protects the database from bad data, regardless of what the application code attempts to do.

**2. Application Simplification**
If a database does not enforce uniqueness on a username, the application must handle it. The application would need to query the database to check if the username exists, and if not, insert it. However, in a highly concurrent environment, two users might try to register with the same username simultaneously. Both application checks might pass before either insert happens, resulting in duplicate usernames! By placing a `UNIQUE` constraint on the database, the database engine handles this concurrency natively. The application simply attempts the insert, catches the constraint violation exception, and informs the user. This simplifies application logic and eliminates race conditions.

**3. Performance and Indexing**
Constraints, particularly `PRIMARY KEY` and `UNIQUE` constraints, automatically generate database indexes. An index is a specialized data structure that significantly improves the speed of data retrieval operations. Because the database knows that a column is unique, it can optimize search algorithms. When querying by a primary key, the database uses an index to locate the record almost instantly (often in O(1) or O(log N) time complexity), rather than scanning the entire table row by row (O(N)).

**4. Documentation and Intent**
Constraints serve as executable documentation. When a new developer looks at a database schema and sees a `CHECK (age >= 18)` constraint, the business rule is immediately apparent and unequivocally enforced. It communicates the intent of the data model clearly to anyone interacting with it.

## Detailed Constraint Analysis and Examples

Let's delve deeper into each of the primary constraint types with extended theoretical context and practical examples.

### The NOT NULL Constraint

By default, any column in SQL can hold a `NULL` value. `NULL` represents the intentional absence of a value; it is not zero, and it is not an empty string. While `NULL` is useful for optional data (like a middle name), it is problematic for mandatory data.

The `NOT NULL` constraint explicitly forbids `NULL` values. If a column is defined as `NOT NULL`, any `INSERT` or `UPDATE` operation that attempts to set the column to `NULL` will fail.

**Common Pitfall:** Developers often forget that empty strings (`''`) and zero (`0`) are valid values that bypass `NOT NULL` constraints. If you want to ensure a string is not empty, you often need to combine `NOT NULL` with a `CHECK` constraint (e.g., `CHECK (length(username) > 0)`).

```sql
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    -- 'bio' can be NULL because we didn't specify NOT NULL
    bio TEXT
);
```

### The UNIQUE Constraint

The `UNIQUE` constraint ensures that no two rows in a table can have the same value for a specified column (or set of columns). This is crucial for identifiers like email addresses, social security numbers, or product SKUs.

**Advanced Edge Case:** In standard SQL (and SQLite), `NULL` values are considered distinct from each other for the purpose of the `UNIQUE` constraint. This means you can insert multiple rows with `NULL` in a `UNIQUE` column, unless the column is also marked `NOT NULL`.

```sql
CREATE TABLE Accounts (
    account_id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE
);
-- You can have multiple accounts without a phone number (NULL),
-- but if a phone number is provided, it must be unique.
```

### The PRIMARY KEY Constraint

The `PRIMARY KEY` is the cornerstone of relational database design. It provides a reliable way to uniquely identify every single record in a table. A table can have only one primary key, although that primary key can consist of multiple columns (a composite primary key).

A primary key automatically implies both `NOT NULL` and `UNIQUE`. In SQLite, an `INTEGER PRIMARY KEY` also generally acts as an auto-incrementing column (aliased to the internal `rowid`).

**Best Practice:** Always define a primary key for every table. While a database might let you create a table without one, doing so prevents reliable updates, deletes, and relationships with other tables.

### The CHECK Constraint

The `CHECK` constraint is incredibly powerful. It allows you to specify an arbitrary boolean expression that must evaluate to `TRUE` or `UNKNOWN` (if a value is NULL) for the data to be accepted. This allows for complex, domain-specific validation right at the database layer.

**Examples of CHECK constraints:**
- Ensuring numerical ranges (e.g., price must be positive).
- Validating string formats (e.g., a status must be 'active', 'inactive', or 'pending').
- Comparing columns within the same row (e.g., an end_date must be greater than or equal to a start_date).

```sql
CREATE TABLE Employees (
    emp_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) CHECK (salary > 0),
    hire_date DATE,
    termination_date DATE,
    -- Table-level check constraint comparing two columns
    CONSTRAINT chk_dates CHECK (termination_date IS NULL OR termination_date >= hire_date)
);
```

### The DEFAULT Constraint

The `DEFAULT` constraint specifies a default value that the database will insert if the `INSERT` statement does not explicitly provide a value for that column. This is useful for flags, timestamps, or common default states.

**Advanced Scenario:** Default values can often be expressions or functions. For example, in many databases, you can use `CURRENT_TIMESTAMP` or `GETDATE()` to automatically stamp a record with the exact time it was created, without the application having to provide the time.

```sql
CREATE TABLE AuditLogs (
    log_id INTEGER PRIMARY KEY,
    action_type VARCHAR(50) NOT NULL,
    -- Automatically set the time the row was inserted
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'success'
);

-- When inserting, we only need to provide the action_type
INSERT INTO AuditLogs (action_type) VALUES ('user_login');
-- created_at and status are automatically populated.
```

## Designing with Constraints: A Comprehensive Example

Let's look at a comprehensive example that combines all these concepts to build a robust table for an e-commerce product catalog.

```sql
CREATE TABLE ECommerceProducts (
    product_id INTEGER PRIMARY KEY,
    -- SKU must exist and be unique across the entire catalog
    sku VARCHAR(20) UNIQUE NOT NULL,
    -- Name cannot be empty
    product_name VARCHAR(200) NOT NULL CHECK (length(product_name) > 0),
    -- Description is optional (can be NULL)
    description TEXT,
    -- Price must be strictly positive
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0.00),
    -- Stock can be zero, but not negative
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    -- Must be one of a specific set of categories
    category VARCHAR(50) NOT NULL CHECK (category IN ('Electronics', 'Clothing', 'Home', 'Books')),
    -- Track when the product was added
    date_added DATE DEFAULT CURRENT_DATE
);
```

In this `ECommerceProducts` table, the constraints create a rigid, highly reliable structure. An application interacting with this database can be confident that if a query returns a product, that product will definitely have a valid positive price, a known category, and a unique SKU. This predictability is the foundation upon which robust, scalable applications are built. 

By mastering constraints, you transition from simply storing data to actively managing and protecting the integrity of your information ecosystem.
