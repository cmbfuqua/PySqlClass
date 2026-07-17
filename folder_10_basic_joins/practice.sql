-- PRACTICE: Basic SQL Joins
-- We will use two tables: `employees` (id, name, department_id) and `departments` (id, name).

-- Example: Get all employees and their department names (only employees with a department)
-- SELECT employees.name, departments.name AS department_name
-- FROM employees
-- INNER JOIN departments ON employees.department_id = departments.id;

-- Exercise 1: INNER JOIN
-- Create a view named `practice_inner_join` that returns the `name` of the employee and the `name` of the department (aliased as `department_name`) using an INNER JOIN.
CREATE VIEW practice_inner_join AS
SELECT employees.name, departments.name AS department_name
FROM employees
-- TODO: Add the INNER JOIN clause here
;

-- Exercise 2: LEFT JOIN
-- Create a view named `practice_left_join` that returns ALL employees and their department names. If an employee does not have a department, the department_name should be NULL.
CREATE VIEW practice_left_join AS
-- TODO: Select employee name and department name (aliased as department_name)
-- TODO: FROM employees
-- TODO: LEFT JOIN departments ON ...
;
