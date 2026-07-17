-- Assignment: Foreign Keys and CRUD
-- You are building a system for a school.

-- We have the 'Teachers' table pre-created for you.
CREATE TABLE Teachers (
    teacher_id INTEGER PRIMARY KEY,
    teacher_name VARCHAR(50)
);

INSERT INTO Teachers (teacher_id, teacher_name) VALUES (1, 'Mr. Smith');
INSERT INTO Teachers (teacher_id, teacher_name) VALUES (2, 'Ms. Johnson');

-- TODO: Create a table named 'Classes'
-- 1. 'class_id' INTEGER PRIMARY KEY
-- 2. 'class_name' VARCHAR(50) NOT NULL
-- 3. 't_id' INTEGER FOREIGN KEY referencing 'teacher_id' in 'Teachers'. Add ON DELETE CASCADE.


-- TODO: Insert two classes. One taught by Mr. Smith (teacher_id 1) and one taught by Ms. Johnson (teacher_id 2).


-- TODO: Update the class name of the class taught by Mr. Smith.


-- TODO: Delete the class taught by Ms. Johnson.

