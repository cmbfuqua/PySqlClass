# Common Table Expressions (CTEs) and Subqueries

## Overview

As you move beyond basic database retrieval and begin performing complex data analysis, you will frequently encounter scenarios where you cannot get your answer in a single, simple step. You might need to filter data based on an aggregated metric (e.g., "Find all employees earning more than the company average"), or you might need to perform multiple layers of joins and aggregations on intermediate datasets.

To solve these complex problems in SQL, we use **Subqueries** and **Common Table Expressions (CTEs)**. Both features allow you to write queries that generate temporary, virtual tables in memory. These temporary result sets can then be immediately referenced and queried by a larger, outer query.

While they achieve similar goals, Subqueries and CTEs have different syntax, different ideal use cases, and distinct impacts on the readability and maintainability of your code.

## Why it's important (Deep Dive)

### 1. Breaking Down Complexity
The primary purpose of CTEs and Subqueries is to break monolithic, impossible-to-read SQL statements into logical, sequential steps. Imagine trying to calculate the month-over-month growth rate of the top 5 highest-grossing products across 3 different regions. Attempting this in one standard query without intermediate steps results in a chaotic, deeply nested block of code that is a nightmare to debug. CTEs allow you to define Step 1, then Step 2 (referencing Step 1), and finally Step 3 (referencing Step 2).

### 2. Deriving Aggregated Filters
A very common analytical requirement is comparing individual rows against aggregate metrics. Standard SQL evaluation order dictates that you cannot use an aggregate function like `AVG()` directly in a `WHERE` clause without a `GROUP BY`, because `WHERE` filters happen *before* aggregations occur. Subqueries bypass this limitation by calculating the aggregate in a separate, nested execution step, and passing the single resulting value back to the main `WHERE` clause.

### 3. Modularity and Reusability
CTEs, in particular, promote modular code. If you define a complex calculation in a CTE at the top of your script, you can join to that CTE multiple times throughout your main query. This adheres to the DRY (Don't Repeat Yourself) principle, ensuring that if the logic needs to change, you only update it in one place.

## Deep Dive: Subqueries

A subquery (also known as an inner query or nested query) is a complete `SELECT` query embedded within a larger `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. 

Subqueries can be categorized by what they return:
- **Scalar Subquery:** Returns exactly one column and one row (a single value).
- **Row Subquery:** Returns one row but multiple columns.
- **Table/Derived Subquery:** Returns multiple rows and columns (a temporary table).

### Subqueries in the WHERE Clause (Scalar)

This is the most common use case. You use a subquery to calculate a single value for a comparison operator (`=`, `>`, `<`).

```sql
-- Find products that cost more than the average product price
SELECT product_name, price
FROM Products
WHERE price > (
    -- This inner query executes first and returns a single number (e.g., 45.50)
    SELECT AVG(price) FROM Products
);
```

### Subqueries with IN and EXISTS (Table)

When a subquery returns a single column but multiple rows, you cannot use `=` or `>`. Instead, you use operators like `IN` or `NOT IN`.

```sql
-- Find customers who have placed an order in the last 7 days
SELECT customer_name, email
FROM Customers
WHERE customer_id IN (
    -- Returns a list of IDs: (10, 45, 992)
    SELECT DISTINCT customer_id 
    FROM Orders 
    WHERE order_date >= date('now', '-7 days')
);
```

### Correlated Subqueries (Advanced)

A standard subquery executes once, independently of the outer query. A **correlated subquery** is different: it references columns from the outer query. This means the inner query is essentially re-evaluated row-by-row for every single row processed by the outer query.

*Warning: Correlated subqueries can be incredibly slow on large datasets because they act like a nested loop (O(N^2) complexity). However, they are powerful for specific row-by-row comparisons.*

```sql
-- Find employees whose salary is above the average salary OF THEIR SPECIFIC DEPARTMENT
SELECT e1.name, e1.salary, e1.department_id
FROM Employees e1
WHERE e1.salary > (
    -- This inner query recalculates for every row in e1
    SELECT AVG(salary) 
    FROM Employees e2 
    -- The correlation happens here:
    WHERE e2.department_id = e1.department_id
);
```

## Deep Dive: Common Table Expressions (CTEs)

A Common Table Expression acts like a temporary, named result set that exists only for the duration of a single SQL statement. They are defined using the `WITH` keyword at the very beginning of the query.

### The Problem with Subqueries: Readability

Subqueries inside the `FROM` clause (often called derived tables) quickly become unreadable. You have to read the query from the inside-out to understand what it does.

```sql
-- A messy derived table subquery
SELECT avg_dept.dept_name, avg_dept.average_salary
FROM (
    SELECT d.dept_name, AVG(e.salary) as average_salary
    FROM Departments d
    JOIN Employees e ON d.dept_id = e.dept_id
    GROUP BY d.dept_name
) AS avg_dept
WHERE avg_dept.average_salary > 60000;
```

### The CTE Solution: Top-Down Logic

CTEs solve this by allowing you to define the temporary tables first, naming them, and then writing a clean main query at the bottom. It allows you to read the logic top-down, just like a normal programming language script.

```sql
-- The exact same logic using a CTE
WITH DepartmentAverages AS (
    SELECT d.dept_name, AVG(e.salary) as average_salary
    FROM Departments d
    JOIN Employees e ON d.dept_id = e.dept_id
    GROUP BY d.dept_name
)
-- The main query is now clean and easy to read
SELECT dept_name, average_salary
FROM DepartmentAverages
WHERE average_salary > 60000;
```

### Chaining Multiple CTEs

One of the most powerful features of the `WITH` clause is the ability to define multiple CTEs, separated by commas. Later CTEs can even reference earlier CTEs!

```sql
WITH 
-- Step 1: Get total sales per region
RegionTotals AS (
    SELECT region_id, SUM(amount) as total_sales
    FROM Sales
    GROUP BY region_id
),
-- Step 2: Find the absolute maximum sales amount across all regions
MaxSales AS (
    SELECT MAX(total_sales) as highest_sales
    FROM RegionTotals
)
-- Step 3: Main query joins them together to find which region(s) hit the max
SELECT r.region_id, r.total_sales
FROM RegionTotals r
JOIN MaxSales m ON r.total_sales = m.highest_sales;
```

## CTEs vs Subqueries: Which to choose?

1. **Readability:** CTEs win hands down. For anything more complex than a simple scalar `WHERE` filter, you should default to a CTE. It makes your code self-documenting.
2. **Reusability:** If you need to reference the exact same derived dataset twice in your main query (e.g., joining to it twice), a CTE allows you to write it once. A subquery would force you to copy-paste the code twice.
3. **Performance:** In modern database engines (PostgreSQL, SQL Server, modern MySQL/SQLite), the query optimizer is usually smart enough to execute a CTE and a Subquery with the exact same execution plan. However, some databases (like older versions of PostgreSQL) would "materialize" (save to a temporary disk table) CTEs, which could be slower for simple queries but faster if the CTE is referenced multiple times. 
4. **Recursion:** CTEs have a unique, advanced capability called `WITH RECURSIVE`, which allows them to reference themselves. This is the only standard SQL way to traverse hierarchical or graph data (like a company organizational chart or a category tree). Standard subqueries cannot do this.

By mastering Subqueries and CTEs, you graduate from writing simple data retrieval scripts to engineering complex, multi-stage data pipelines entirely within SQL.
