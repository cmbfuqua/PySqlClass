-- Assignment: Bridge Tables

-- Setup: Doctors and Patients
CREATE TABLE Doctors (
    doctor_id INTEGER PRIMARY KEY,
    doctor_name VARCHAR(50)
);

CREATE TABLE Patients (
    patient_id INTEGER PRIMARY KEY,
    patient_name VARCHAR(50)
);

INSERT INTO Doctors VALUES (1, 'Dr. Smith'), (2, 'Dr. Jones');
INSERT INTO Patients VALUES (100, 'Alice'), (101, 'Bob'), (102, 'Charlie');

-- TODO: Create a bridge table named 'Appointments'
-- 1. 'doc_id' INTEGER FOREIGN KEY referencing Doctors(doctor_id) ON DELETE CASCADE
-- 2. 'pat_id' INTEGER FOREIGN KEY referencing Patients(patient_id) ON DELETE CASCADE
-- 3. 'appointment_date' DATE
-- 4. Composite PRIMARY KEY on (doc_id, pat_id, appointment_date)


-- TODO: Insert the following appointments:
-- Dr. Smith (1) sees Alice (100) on '2023-10-01'
-- Dr. Smith (1) sees Bob (101) on '2023-10-01'
-- Dr. Jones (2) sees Alice (100) on '2023-10-02'


