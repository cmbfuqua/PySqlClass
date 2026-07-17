-- PRACTICE: Complex Joins
-- Example: CROSS JOIN
-- SELECT p.product_name, s.size_name FROM products p CROSS JOIN sizes s;

-- Example: Self Join
-- SELECT a.name, b.name AS manager FROM employees a LEFT JOIN employees b ON a.manager_id = b.id;

-- EXERCISE 1: CROSS JOIN
-- We have tables `colors` (id, color_name) and `sizes` (id, size_name).
-- Create a view named `all_combinations` that returns the cartesian product of colors and sizes.
-- The columns should be color_name and size_name.
CREATE VIEW all_combinations AS
SELECT 
    -- TODO: Select color_name and size_name
    
FROM colors c
-- TODO: Perform the correct join with sizes table
;

-- EXERCISE 2: Self Join
-- We have a table `employees` (id, name, manager_id).
-- Create a view named `employee_managers` that returns employee name and their manager's name.
-- The columns should be employee_name and manager_name.
CREATE VIEW employee_managers AS
-- TODO: Write the self join query
;
