-- Вставка данных в таблицу Education
INSERT INTO Education (EducationName) VALUES
('High School'),
('Associate Degree'),
('Bachelor’s Degree'),
('Master’s Degree'),
('Doctorate');

-- Вставка данных в таблицу Departments
INSERT INTO Departments (DepartmentName) VALUES
('Human Resources'),
('Engineering'),
('Sales'),
('Marketing'),
('Customer Support');

-- Вставка данных в таблицу Positions
INSERT INTO Positions (PositionName, Salary) VALUES
('Intern', 15000.00),
('Junior Developer', 45000.00),
('Senior Developer', 85000.00),
('Manager', 95000.00),
('Director', 125000.00);

-- Вставка данных в таблицу Employees
INSERT INTO Employees (FirstName, EducationID, DepartmentID, PositionID) VALUES
('Alice Johnson', 3, 2, 2), -- Bachelor’s Degree, Engineering, Junior Developer
('Bob Smith', 4, 2, 3), -- Master’s Degree, Engineering, Senior Developer
('Charlie Brown', 2, 1, 1), -- Associate Degree, Human Resources, Intern
('Diana Prince', 5, 4, 4), -- Doctorate, Marketing, Manager
('Ethan Hunt', 3, 3, 5); -- Bachelor’s Degree, Sales, Director

-- Вставка данных в таблицу History
INSERT INTO History (EmployeeID, PositionID, Date) VALUES
(1, 2, '2023-01-15'), -- Alice Johnson starts as Junior Developer
(2, 3, '2022-11-01'), -- Bob Smith starts as Senior Developer
(3, 1, '2023-06-01'), -- Charlie Brown starts as Intern
(4, 4, '2021-03-10'), -- Diana Prince starts as Manager
(5, 5, '2020-08-25'); -- Ethan Hunt starts as Director
