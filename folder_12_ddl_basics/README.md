# Folder 12: Data Definition Language (DDL) Basics

## 1. Introduction to DDL

Data Definition Language (DDL) is a core subset of SQL (Structured Query Language) that is exclusively used to define, manage, and modify the underlying structures in a database management system. While other parts of SQL—like Data Manipulation Language (DML)—focus on the actual data (inserting rows, querying values, updating records), DDL focuses entirely on the *containers* that hold that data. 

Think of a database like a giant filing cabinet. DDL is the set of instructions you use to build the cabinet, create the drawers, label those drawers, and set rules for what kind of folders can go inside them. DML, on the other hand, is the process of actually putting folders into the drawers. 

In the context of relational databases, DDL commands are used to create, modify, and delete database objects such as:
- **Tables**: The primary data storage structures, consisting of columns and rows.
- **Indexes**: Data structures that improve the speed of data retrieval operations.
- **Views**: Virtual tables based on the result-set of an SQL statement.
- **Triggers, Procedures, and Functions**: Programmatic constructs stored in the database.

For the purpose of these basics, we will focus primarily on **Tables**, as they are the fundamental building blocks of any relational database schema. The three cornerstone commands of DDL are `CREATE`, `ALTER`, and `DROP`.

## 2. Deep Dive: Why is DDL Important?

Understanding and mastering DDL is arguably one of the most critical skills for a backend developer, data engineer, or database administrator. Here is a deep dive into why careful schema design using DDL is so important:

### 2.1. Enforcing Data Integrity
The strongest defense against bad data is a well-defined schema. When you define a table using DDL, you aren't just naming columns; you are establishing strict rules (constraints) about what data is acceptable. For example, if you define a column as `INTEGER`, the database will prevent text from being stored there (subject to dialect-specific rules, like SQLite's type affinity). If you mark a column as `NOT NULL`, it is impossible to save a record without providing that piece of information. This shifts the burden of data validation from your application code directly to the database engine, providing a bulletproof layer of security against malformed data.

### 2.2. Structural Clarity and Documentation
A well-written DDL script serves as living documentation for your application's domain model. By looking at the `CREATE TABLE` statements, a new developer can instantly understand the core entities of the system, their attributes, and how they relate to one another. The DDL script essentially translates abstract business requirements into a concrete, executable contract.

### 2.3. Query Optimization and Performance Foundation
While DDL doesn't write the queries, the structures it creates dictate how efficiently those queries will run. Choosing the right data types (e.g., using a tiny integer instead of a massive string for a status code) saves disk space and memory. Establishing primary keys and foreign keys automatically creates indexes in many database engines, which dramatically speeds up lookups and table joins. A poor DDL design will lead to performance bottlenecks that no amount of query optimization (DML) can fully fix.

## 3. Core DDL Commands in Detail

Let's explore the primary DDL commands, focusing heavily on standard SQL with considerations for SQLite, which we use in our practice environments.

### 3.1. The `CREATE` Command

The `CREATE` command is used to build new objects in the database. The most common usage is `CREATE TABLE`.

#### 3.1.1. Basic Syntax
```sql
CREATE TABLE table_name (
    column1_name data_type constraints,
    column2_name data_type constraints,
    ...
);
```

#### 3.1.2. SQLite Data Types and Type Affinity
Unlike standard SQL which enforces strict typing, SQLite uses a dynamic typing system called "Type Affinity". The data type is associated with the value itself, not just the column. However, SQLite still assigns an affinity to columns based on the declared type. The five storage classes in SQLite are:
- **NULL**: The value is a NULL value.
- **INTEGER**: A signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
- **REAL**: A floating point value, stored as an 8-byte IEEE floating point number.
- **TEXT**: A text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
- **BLOB**: A blob of data, stored exactly as it was input.

#### 3.1.3. Constraints
Constraints are rules applied to columns.
- **PRIMARY KEY**: Uniquely identifies each row. In SQLite, an `INTEGER PRIMARY KEY` automatically becomes an auto-incrementing column (an alias for the `rowid`).
- **NOT NULL**: Ensures that a column cannot have a NULL value.
- **UNIQUE**: Ensures that all values in a column are different.
- **DEFAULT**: Sets a default value for a column if no value is specified during an insert.
- **CHECK**: Ensures that the values in a column satisfy a specific condition.

#### Example: Creating a Robust Table
```sql
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 18),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```
*Note the use of `IF NOT EXISTS`. This is a crucial defensive programming technique in DDL scripts to prevent errors if the script is run multiple times.*

### 3.2. The `ALTER` Command

The `ALTER TABLE` command modifies the structure of an existing table without deleting the data it contains.

#### 3.2.1. Basic Capabilities
You can use `ALTER TABLE` to add new columns, rename the table, or rename columns.

```sql
-- Adding a new column
ALTER TABLE users ADD COLUMN last_login_date TEXT;

-- Renaming a table
ALTER TABLE users RENAME TO system_users;

-- Renaming a column (Supported in SQLite 3.25.0+)
ALTER TABLE system_users RENAME COLUMN age TO user_age;
```

#### 3.2.2. The SQLite ALTER Limitation
It is vital to understand that SQLite has historically had very limited support for `ALTER TABLE`. While modern versions allow renaming columns and dropping columns, older versions (or other database engines in specific strict modes) might not support dropping or altering the data type of an existing column directly. 

**The Table Recreation Pattern:**
When a direct `ALTER TABLE` is not supported, you must use the 12-step table recreation pattern:
1. `PRAGMA foreign_keys=off;`
2. `BEGIN TRANSACTION;`
3. `CREATE TABLE new_table (...)`
4. `INSERT INTO new_table SELECT ... FROM old_table;`
5. `DROP TABLE old_table;`
6. `ALTER TABLE new_table RENAME TO old_table;`
7. Recreate indexes and triggers.
8. `PRAGMA foreign_key_check;`
9. `COMMIT;`
10. `PRAGMA foreign_keys=on;`

### 3.3. The `DROP` Command

The `DROP TABLE` command completely removes a table and all of its data from the database. This is a destructive and irreversible operation (unless you have backups or are operating within an uncommitted transaction).

```sql
DROP TABLE users;
```

#### Defending Against Errors
Similar to `CREATE`, you should use `IF EXISTS` to prevent errors when trying to drop a table that might not be there.

```sql
DROP TABLE IF EXISTS users;
```

## 4. Common Pitfalls and Edge Cases

When working with DDL, developers frequently encounter several traps:

### 4.1. The "Type Affinity" Trap in SQLite
Because SQLite is dynamically typed, it will allow you to insert a string like `'hello'` into an `INTEGER` column if you force it, or it will implicitly convert the string `'123'` into the integer `123`. Developers coming from strict databases like PostgreSQL often assume their SQLite DDL is enforcing strict typing when it isn't. You must rely on `CHECK` constraints (e.g., `CHECK(typeof(my_column) = 'integer')`) if you want strict enforcement in SQLite.

### 4.2. Dropping Tables with Foreign Keys
If Table B has a foreign key referencing Table A, dropping Table A can lead to orphaned records in Table B or structural inconsistencies. In SQLite, if `PRAGMA foreign_keys = ON` is set, dropping Table A will result in an error if it violates foreign key constraints. Always be aware of the dependency graph of your tables before dropping them.

### 4.3. Forgetting `IF NOT EXISTS` in Migration Scripts
When writing SQL scripts intended to setup a database (like the ones you will write in these exercises), failing to use `IF NOT EXISTS` means your script will crash on the second run. Idempotency (the ability to run a script multiple times with the same result) is a key best practice in DDL scripting.

### 4.4. The Auto-Increment Confusion
In standard SQL, you might use `AUTO_INCREMENT` or `SERIAL`. In SQLite, simply defining a column as `INTEGER PRIMARY KEY` automatically makes it auto-incrementing. Adding the `AUTOINCREMENT` keyword in SQLite actually changes the underlying algorithm to prevent reusing deleted IDs, which adds CPU and memory overhead and is generally not recommended unless strictly necessary for business logic.

## 5. Extended Examples: Building a Complex Schema

To cement these concepts, let's look at an extended example of building a schema for a simple E-Commerce system. This demonstrates how tables relate to one another and how various constraints are applied.

### E-Commerce Schema Example

```sql
-- 1. Create the Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    registration_date TEXT DEFAULT CURRENT_DATE
);

-- 2. Create the Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL CHECK (price > 0), -- Price must be strictly positive
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0)
);

-- 3. Create the Orders Table (References Customers)
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'PENDING',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

-- 4. Create the Order_Items Junction Table (Many-to-Many Relationship)
CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price > 0),
    PRIMARY KEY (order_id, product_id), -- Compound Primary Key
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);
```

### Analysis of the Example
- **Data Integrity**: The `price`, `stock_quantity`, and `quantity` columns all have `CHECK` constraints to ensure impossible values (like negative stock) cannot enter the system.
- **Relationships**: The `order_items` table acts as a bridge between `orders` and `products`. It uses a **Compound Primary Key** (`PRIMARY KEY (order_id, product_id)`), ensuring that the same product cannot be added twice to the exact same order as separate line items (instead, the quantity should be updated).
- **Cascading Actions**: The `ON DELETE CASCADE` rule in `order_items` means that if an `order` is dropped from the database, all its associated line items are automatically deleted, preventing orphan data. Conversely, `ON DELETE RESTRICT` on the product reference prevents a product from being deleted if it has been part of an order.

## 6. Summary and Next Steps

DDL is the architectural blueprint of your application. By mastering `CREATE`, `ALTER`, and `DROP`, along with a deep understanding of data types and constraints, you are equipping yourself to build robust, scalable, and secure data storage systems.

In this module, you will practice these concepts directly. Start with `practice.sql` to get a feel for the syntax, and then move on to `assignment.sql` to build a schema from scratch based on a set of business requirements.
