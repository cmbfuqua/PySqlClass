-- Practice: Database Constraints
-- Example: Creating a table with basic constraints
/*
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) CHECK (price > 0)
);
*/

-- TODO: Create a table named 'Employees' with the following constraints:
-- 1. 'emp_id' as an INTEGER PRIMARY KEY
-- 2. 'email' as a VARCHAR(100) that must be UNIQUE and NOT NULL
-- 3. 'salary' as an INTEGER that must be greater than 30000 (CHECK constraint)
-- 4. 'department' as a VARCHAR(50) with a DEFAULT value of 'Engineering'

CREATE TABLE Employees (
    -- Your code here
    
);
