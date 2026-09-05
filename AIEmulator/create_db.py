# Create imports to use SQLite and OS
import sqlite3
import os

# Tie to OS, double-check if "data" folder exists there
os.makedirs("data", exist_ok=True)

# Create connection and cursor variables, initialize to None
conn = None
cursor = None

# Create Try block to be able to catch exceptions
try:
    # Connect to the database, establish sample.db
    conn = sqlite3.connect("data/sample.db")
    cursor = conn.cursor()
    print("✅ Successfully connected to 'sample.db' in 'data/' directory.")

    # Drop tables in case they exist
    tables = ['timesheets', 'employee_projects', 'projects', 'employees', 'departments']
    for t in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {t};")

    # Create table 'departments', initialize 'id' as Primary Key, set 'name' with TEXT
    cursor.execute("""CREATE TABLE departments (
        id INTEGER PRIMARY KEY, 
        name TEXT
    );""")

    # Create table 'employees', initialize 'id' as Primary Key, set 'name' and 'role' with TEXT, define 'salary' with
    # REAL to indicate float numeric values. Assign 'department_id' as Foreign Key to point to 'id' in 'departments'
    # table
    cursor.execute("""CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        salary REAL,
        department_id INTEGER,
        FOREIGN KEY(department_id) REFERENCES departments(id)
    );""")

    # Create table 'projects', initialize 'id' as Primary Key, set 'name' with TEXT, define 'budget' with
    # REAL to indicate float numeric values.
    cursor.execute("""CREATE TABLE projects (
        id INTEGER PRIMARY KEY, 
        name TEXT, 
        budget REAL
    );""")

    # Create table 'employee_projects', initialize 'employee_id' and 'project_id' as Primary Key,
    # set them as Foreign Keys to point to 'id' in both 'employees' and 'projects' tables
    cursor.execute("""CREATE TABLE employee_projects (
        employee_id INTEGER,
        project_id INTEGER,
        FOREIGN KEY(employee_id) REFERENCES employees(id),
        FOREIGN KEY(project_id) REFERENCES projects(id)
    );""")

    # Create table 'timesheets', initialize 'id' as Primary Key, set 'employee_id' and 'project_id' as integers (and
    # as foreign keys to point to 'id' in both 'employees' and 'projects' tables), declare 'hours_worked' as REAL to
    # indicate float numeric values, make date as 'TEXT' as Foreign Keys to point to 'id' in both 'employees' and
    # 'projects' tables
    cursor.execute("""CREATE TABLE timesheets (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        project_id INTEGER,
        hours_worked REAL,
        date TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(id),
        FOREIGN KEY(project_id) REFERENCES projects(id)
    );""")

    # Insert 'id' and 'name' data into 'departments' table
    cursor.executemany("INSERT INTO departments (id, name) VALUES (?, ?)", [
        (1, "Engineering"),
        (2, "HR"),
        (3, "Finance")
    ])

    # Insert 'id', 'name', 'role', 'salary', and 'department_id' data into 'employees' table
    cursor.executemany("INSERT INTO employees (id, name, role, salary, department_id) VALUES (?, ?, ?, ?, ?)", [
        (1, "Alice", "Engineer", 85000, 1),
        (2, "Bob", "Manager", 95000, 1),
        (3, "Charlie", "HR Specialist", 60000, 2),
        (4, "Diana", "Accountant", 70000, 3)
    ])

    # Insert 'id', 'name', and 'budget' data into 'projects' table
    cursor.executemany("INSERT INTO projects (id, name, budget) VALUES (?, ?, ?)", [
        (1, "Project X", 50000),
        (2, "Project Y", 120000)
    ])

    # Insert 'employee_id' and 'project_id' data into 'employee_projects' table
    cursor.executemany("INSERT INTO employee_projects (employee_id, project_id) VALUES (?, ?)", [
        (1,1),(2,1),(2,2),(3,2),(4,2)
    ])

    # Insert 'employee_id', 'project_id', 'hours_worked', and 'date' data into 'timesheets' table
    cursor.executemany("INSERT INTO timesheets (employee_id, project_id, hours_worked, date) VALUES (?, ?, ?, ?)", [
        (1,1,10,"2025-08-18"),
        (2,1,12,"2025-08-18"),
        (2,2,8,"2025-08-18"),
        (3,2,7,"2025-08-18"),
        (4,2,9,"2025-08-18")
    ])

    # Commit changes
    conn.commit()
    print("✅ Database operations completed successfully.")

# Handle exceptions for Try block
except sqlite3.Error as e:
    print("❌ Error with database operation:", e)
    if conn:
        conn.rollback()
finally:
    # Clean up resources
    if cursor:
        cursor.close()
    if conn:
        conn.close()