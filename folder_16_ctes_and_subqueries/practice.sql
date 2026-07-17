-- Practice: CTEs and Subqueries

-- Setup: Sales Data
CREATE TABLE Sales (
    sale_id INTEGER PRIMARY KEY,
    employee_name VARCHAR(50),
    amount DECIMAL(10, 2)
);

INSERT INTO Sales VALUES (1, 'Alice', 500);
INSERT INTO Sales VALUES (2, 'Bob', 300);
INSERT INTO Sales VALUES (3, 'Alice', 700);
INSERT INTO Sales VALUES (4, 'Charlie', 400);

-- TODO: Write a query using a SUBQUERY to find the names of employees who have made a sale greater than 450.
-- Return the employee_name only.

-- Your code here


-- TODO: Write a query using a CTE to find the total sales per employee, 
-- and then select only those employees whose total sales exceed 600.
-- Return employee_name and total_sales.

-- Your code here
