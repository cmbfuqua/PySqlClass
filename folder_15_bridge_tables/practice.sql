-- Practice: Bridge Tables

-- Setup: Actors and Movies
CREATE TABLE Actors (
    actor_id INTEGER PRIMARY KEY,
    actor_name VARCHAR(50)
);

CREATE TABLE Movies (
    movie_id INTEGER PRIMARY KEY,
    movie_title VARCHAR(50)
);

INSERT INTO Actors VALUES (1, 'Tom Hanks'), (2, 'Meryl Streep');
INSERT INTO Movies VALUES (10, 'The Post'), (11, 'Forrest Gump');

-- TODO: Create a bridge table named 'ActorMovies' to link Actors and Movies.
-- 1. 'a_id' INTEGER FOREIGN KEY referencing Actors(actor_id) ON DELETE CASCADE
-- 2. 'm_id' INTEGER FOREIGN KEY referencing Movies(movie_id) ON DELETE CASCADE
-- 3. Composite PRIMARY KEY using (a_id, m_id)

CREATE TABLE ActorMovies (
    -- Your code here
    
);

-- TODO: Insert records to show that Tom Hanks (1) and Meryl Streep (2) both acted in 'The Post' (10).
-- Also, Tom Hanks (1) acted in 'Forrest Gump' (11).


