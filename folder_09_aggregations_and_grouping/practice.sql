-- Aggregations and Grouping Practice
-- 
-- Example: 
-- CREATE VIEW employee_counts AS 
-- SELECT department, COUNT(*) as count FROM employees GROUP BY department;

-- We have a table `sales` with columns: `id`, `product_category`, `revenue`, `region`.
-- TODO: Create a view named `category_revenue` that calculates the total revenue for each `product_category`.
CREATE VIEW category_revenue AS
SELECT product_category, SUM(____) AS total_revenue
FROM sales
GROUP BY ____;

-- TODO: Create a view named `region_stats` that calculates the average revenue, min revenue, and max revenue per region.
CREATE VIEW region_stats AS
SELECT 
    ____, 
    AVG(____) AS avg_revenue,
    ____(____) AS min_revenue,
    ____ AS max_revenue
FROM sales
____ ____;
