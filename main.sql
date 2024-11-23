CREATE TABLE Education (
    EducationID serial PRIMARY KEY,
    EducationName varchar(100) NOT NULL
);

CREATE TABLE Departments (
    DepartmentID serial PRIMARY KEY,
    DepartmentName varchar(100) NOT NULL
);

CREATE TABLE Positions (
    PositionID serial PRIMARY KEY,
    PositionName varchar(100) NOT NULL,
    Salary numeric(10, 2) NOT NULL CHECK (Salary >= 0)
);

CREATE TABLE Employees (
    EmployeeID serial PRIMARY KEY,
    FirstName varchar(100) NOT NULL,
    EducationID int NOT NULL,
    DepartmentID int NOT NULL,
    PositionID int NOT NULL,
    FOREIGN KEY (PositionID) REFERENCES Positions(PositionID),
    FOREIGN KEY (EducationID) REFERENCES Education(EducationID),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

CREATE TABLE History (
    HistoryID serial PRIMARY KEY,
    EmployeeID int NOT NULL,
    PositionID int NOT NULL,
    Date date NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (PositionID) REFERENCES Positions(PositionID)
);
