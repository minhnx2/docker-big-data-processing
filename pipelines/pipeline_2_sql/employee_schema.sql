CREATE TABLE IF NOT EXISTS employees (
    "Serial Number" NUMERIC PRIMARY KEY,
    "Company Name" TEXT,
    "Employee Markme" TEXT,
    "Description" TEXT,
    "Leave" INTEGER
);

DROP TABLE IF EXISTS employees_temp;
CREATE TABLE employees_temp (
    "Serial Number" NUMERIC PRIMARY KEY,
    "Company Name" TEXT,
    "Employee Markme" TEXT,
    "Description" TEXT,
    "Leave" INTEGER
);