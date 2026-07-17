-- Practice: Foreign Keys and CRUD

-- Setup: We have a parent table 'Categories'
CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(50)
);

INSERT INTO Categories (category_id, category_name) VALUES (1, 'Electronics');
INSERT INTO Categories (category_id, category_name) VALUES (2, 'Books');

-- TODO: Create a table 'Items'
-- 1. 'item_id' INTEGER PRIMARY KEY
-- 2. 'name' VARCHAR(50)
-- 3. 'cat_id' INTEGER that is a FOREIGN KEY referencing 'category_id' in 'Categories'
CREATE TABLE Items (
    -- Your code here
    
);

-- TODO: Insert an item into the 'Items' table (e.g., a 'Laptop' in the 'Electronics' category)
-- Your code here

-- TODO: Update the name of the item you just inserted
-- Your code here

-- TODO: Delete the item you just updated
-- Your code here
