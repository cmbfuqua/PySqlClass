-- Assignment: CTEs and Subqueries

-- Setup: Orders and Customers
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(50)
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_total DECIMAL(10, 2)
);

INSERT INTO Customers VALUES (1, 'Company A');
INSERT INTO Customers VALUES (2, 'Company B');
INSERT INTO Customers VALUES (3, 'Company C');

INSERT INTO Orders VALUES (101, 1, 1500);
INSERT INTO Orders VALUES (102, 1, 2000);
INSERT INTO Orders VALUES (103, 2, 500);
INSERT INTO Orders VALUES (104, 3, 3000);

-- TODO: 1. Use a SUBQUERY to find the customer_name of the customer who placed order_id 103.

-- Your code here


-- TODO: 2. Use a CTE to calculate the total amount spent by each customer_id. 
-- Then, join this CTE with the Customers table to return customer_name and total_spent
-- for customers who spent more than 1000 in total.

-- Your code here
