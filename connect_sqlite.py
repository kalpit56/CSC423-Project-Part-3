import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

tablesCreated = False
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if(len(tables) == 7):
    tablesCreated = True

# String variable for passing queries to cursor
createTables = ["""
    CREATE TABLE Department(
    department_name VARCHAR(255) NOT NULL CHECK(department_name LIKE 'Department of %'),
    chair_name VARCHAR(255),
    num_of_faculty INT,
    PRIMARY KEY(department_name)
    );
    """,
    """
    CREATE TABLE Major(
        major_code CHAR(3) NOT NULL,
        major_name VARCHAR(255) UNIQUE NOT NULL,
        department_name VARCHAR(255),
        PRIMARY KEY(major_code),
        FOREIGN KEY(department_name) REFERENCES Department(department_name) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE Student(
        stu_id INT NOT NULL,
        stu_name VARCHAR(255),
        stu_initials VARCHAR(3) CHECK(length(stu_initials) > 1),
        PRIMARY KEY(stu_id),
        CHECK(LENGTH(stu_initials) > 1)
    );
    """, 
    """
    CREATE TABLE Event(
        event_num INT NOT NULL,
        event_name VARCHAR(255) UNIQUE NOT NULL,
        start_date DATE CHECK(start_date > Current_date) UNIQUE NOT NULL,
        end_date DATE,
        PRIMARY KEY(event_num),
        CONSTRAINT GREATER CHECK (end_date > start_date)
    );
    """,
    """
    CREATE TABLE Hosting(
        department_name VARCHAR(255) NOT NULL,
        event_name VARCHAR(255) NOT NULL,
        PRIMARY KEY(department_name, event_name),
        FOREIGN KEY(department_name) REFERENCES Department(department_name),
        FOREIGN KEY(event_name) REFERENCES Event(event_name)
    );
    """, 
    """
    CREATE TABLE Declaring(
        major_code VARCHAR(3) NOT NULL,
        stu_id INT NOT NULL,
        PRIMARY KEY(major_code, stu_id),
        FOREIGN KEY(major_code) REFERENCES Major(major_code),
        FOREIGN KEY(stu_id) REFERENCES Student(stu_id)
    );
    """, 
    """
    CREATE TABLE Attending(
        stu_id INT NOT NULL,
        event_num INT NOT NULL,
        PRIMARY KEY(stu_id, event_num),
        FOREIGN KEY(stu_id) REFERENCES Student(stu_id),
        FOREIGN KEY(event_num) REFERENCES Event(event_num)
    );
    """
    ]

# Execute query, the result is stored in cursor
if(tablesCreated == False):
    for entry in createTables:
        cursor.execute(entry)


departmentTuples = [
    """
    INSERT INTO Department VALUES('Department of Computer Science', 'Geoff Sutcliffe', 25);
    """,
    """
    INSERT INTO Department VALUES('Department of Marketing', 'John Smith', 50);
    """,
    """
    INSERT INTO Department VALUES('Department of Mathematics', 'John Doe', 43);
    """,
    """
    INSERT INTO Department VALUES('Department of Interactive Media', 'Robert Brown', 82);
    """,
    """
    INSERT INTO Department VALUES('Department of Biology', 'Mary Williams', 101);
    """
]

majorTuples = [
    """
    INSERT INTO Major VALUES('CSC', 'Computer Science', 'Department of Computer Science');
    """,
    """
    INSERT INTO Major VALUES('CMK', 'Corporate Marketing', 'Department of Marketing');
    """,
    """
    INSERT INTO Major VALUES('BIO', 'Biology', 'Department of Biology');
    """,
    """
    INSERT INTO Major VALUES('MTH', 'Mathematics', 'Department of Mathematics');
    """,
    """
    INSERT INTO Major VALUES('GDS', 'Game Design', 'Department of Interactive Media');
    """
]

studentTuples = [
    """
    INSERT INTO Student VALUES(0248, 'Anish Patel', 'AP');
    """,
    """
    INSERT INTO Student VALUES(6487, 'Kalpit Mody', 'KM');
    """,
    """
    INSERT INTO Student VALUES(0001, 'Dan Smith', 'DS');
    """,
    """
    INSERT INTO Student VALUES(2849, 'Aaroh Patel', 'AP');
    """,
    """
    INSERT INTO Student VALUES(0302, 'Auric Saha', 'AS');
    """
]

eventTuples = [
    """
    INSERT INTO Event VALUES(001, 'Valentine Day Event', '2022-02-14', '2022-02-15');
    """,
    """
    INSERT INTO Event VALUES(002, 'Homecoming', '2022-11-01', '2022-11-08');
    """,
    """
    INSERT INTO Event VALUES(003, 'Graduation', '2022-05-13', '2022-05-14');
    """,
    """
    INSERT INTO Event VALUES(004, 'Club Fair', '2021-12-17', '2022-01-18');
    """,
    """
    INSERT INTO Event VALUES(005, 'Major Advising', '2022-03-12', '2022-03-20');
    """
]

hostingTuples = [
    """
    INSERT INTO Hosting VALUES('Department of Interactive Media', 'Valentine Day Event');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Marketing', 'Homecoming');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Computer Science', 'Graduation');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Biology', 'Club Fair');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Computer Science', 'Club Fair');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Mathematics', 'Major Advising');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Marketing', 'Graduation');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Biology', 'Graduation');
    """,
    """
    INSERT INTO Hosting VALUES('Department of Interactive Media', 'Graduation');
    """
]

decalringTuples = [
    """
    INSERT INTO Declaring VALUES('CSC', 6487);
    """,
    """
    INSERT INTO Declaring VALUES('CMK', 0248);
    """,
    """
    INSERT INTO Declaring VALUES('GDS', 6487);
    """,
    """
    INSERT INTO Declaring VALUES('MTH', 0302);
    """,
    """
    INSERT INTO Declaring VALUES('BIO', 2849);
    """,
    """
    INSERT INTO Declaring VALUES('CSC', 0001);
    """
]

attendingTuples = [
    """
    INSERT INTO Attending VALUES(6487, 003);
    """,
    """
    INSERT INTO Attending VALUES(0001, 004);
    """,
    """
    INSERT INTO Attending VALUES(0248, 004);
    """,
    """
    INSERT INTO Attending VALUES(0302, 003);
    """,
    """
    INSERT INTO Attending VALUES(2849, 005);
    """,
    """
    INSERT INTO Attending VALUES(0001, 005);
    """
]

allTuples = [departmentTuples, majorTuples, studentTuples, eventTuples, hostingTuples, decalringTuples, attendingTuples]

for relations in allTuples:
    for tuples in relations:
        cursor.execute(tuples)

print()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()


printEachTableQueries = [
    """
    SELECT * FROM Department;
    """,
    """
    SELECT * FROM Major;
    """,
    """
    SELECT * FROM Student;
    """,
    """
    SELECT * FROM Event;
    """,
    """
    SELECT * FROM Hosting;
    """,
    """
    SELECT * FROM Declaring;
    """,
    """
    SELECT * FROM Attending;
    """
]

print("Snapshot of tables after all example tuples have been inserted: ")
print()
for(entry, table) in zip(printEachTableQueries, tables):
    cursor.execute(entry)
    print(table)
    column_names = [row[0] for row in cursor.description]

    # Fetch data and load into a pandas dataframe
    table_data = cursor.fetchall()
    df = pd.DataFrame(table_data, columns=column_names)

    # Examine dataframe
    print(df)
    print()


queryAnswers = [
    """
    SELECT event_name
    FROM Event e, Attending a
    WHERE a.stu_id = 0001 AND a.event_num = e.event_num;
    """,
    """
    SELECT SUM(num_of_faculty)
    FROM Department;
    """,
    """
    SELECT s.stu_name, m.major_name, m.department_name
    FROM Declaring d, Major m, Student s
    WHERE d.major_code = m.major_code AND d.stu_id = s.stu_id
    GROUP BY s.stu_name;
    """,
    """
    SELECT h.event_name, COUNT(h.department_name)
    FROM Hosting h, Department d
    WHERE d.department_name = h.department_name
    GROUP BY h.event_name;
    """,
    """
    SELECT major_name, chair_name
    FROM Department d, Major m
    WHERE m.department_name = d.department_name
    GROUP BY major_name;
    """,
    """
    SELECT e.event_name, d.department_name, d.chair_name
    FROM Event e, Department d, Hosting h
    WHERE e.start_date > '2022-03-31' AND e.event_name = h.event_name AND h.department_name = d.department_name
    GROUP BY e.event_name;
    """,
    """
    SELECT COUNT(stu_id) AS NUM_OF_STUDENTS
    FROM Attending
    WHERE event_num = 004;
    """
]

queryQuestions = [
    "List all the events that the student with the stu_id 0001 attended.",
    "How many faculty members are there in the university?",
    "List the name of the major and department of the major that each student has declared.",
    "List the number of departments that host each event.",
    "List the chair names of each major.",
    "List the event name, department name, and chair of department for all events that are scheduled after March 2022.",
    "How many people attended event 004?"
]

print("Example queries: ")
print()
for (solutions, questions) in zip(queryAnswers, queryQuestions):
    cursor.execute(solutions)
    print()
    print(questions)
    print()
    column_names = [row[0] for row in cursor.description]
    table_data = cursor.fetchall()
    df = pd.DataFrame(table_data, columns=column_names)

    # Examine dataframe
    print(df)

# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
