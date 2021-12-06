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
if(len(tables) > 0):
    tablesCreated = True

# dropList = ["DROP TABLE Department"]

# String variable for passing queries to cursor
query = ["""
    CREATE TABLE Department(
    department_name VARCHAR(255) NOT NULL,
    chair_name VARCHAR(255),
    num_of_faculty INT,
    PRIMARY KEY(department_name)
    );
    """,
    """
    CREATE TABLE Major(
        major_code VARCHAR(3) NOT NULL,
        major_name VARCHAR(255) NOT NULL,
        department_name VARCHAR(255),
        PRIMARY KEY(major_code),
        FOREIGN KEY(department_name) REFERENCES Department(department_name) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE Student(
        stu_id INT NOT NULL,
        stu_name VARCHAR(255),
        stu_initials VARCHAR(3),
        PRIMARY KEY(stu_id),
        CHECK(LENGTH(stu_initials) > 1)
    );
    """, 
    """
    CREATE TABLE Event(
        event_num INT NOT NULL,
        event_name VARCHAR(255),
        start_date DATE CHECK(start_date > Current_date),
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
        FOREIGN KEY(department_name) REFERENCES Department(department_name) ON DELETE SET NULL,
        FOREIGN KEY(event_name) REFERENCES Event(event_name) ON DELETE SET NULL
    );
    """, 
    """
    CREATE TABLE Declaring(
        major_code VARCHAR(3) NOT NULL,
        stu_id INT NOT NULL,
        PRIMARY KEY(major_code, stu_id),
        FOREIGN KEY(major_code) REFERENCES Major(major_code) ON DELETE SET NULL,
        FOREIGN KEY(stu_id) REFERENCES Student(stu_id) ON DELETE SET NULL
    );
    """, 
    """
    CREATE TABLE Attending(
        stu_id INT NOT NULL,
        event_num INT NOT NULL,
        PRIMARY KEY(stu_id, event_num),
        FOREIGN KEY(stu_id) REFERENCES Student(stu_id) ON DELETE SET NULL,
        FOREIGN KEY(event_num) REFERENCES Event(event_num) ON DELETE SET NULL
    );
    """,
    ]

# Execute query, the result is stored in cursor
if(tablesCreated == False):
    for entry in query:
        print(entry)
        cursor.execute(entry)



departmentTuples = [
    """
    INSERT INTO Department VALUES('Computer Science', 'Geoff Sutcliffe', 25);
    """,
    """
    INSERT INTO Department VALUES('Marketing', 'John Smith', 50);
    """,
    """
    INSERT INTO Department VALUES('Mathematics', 'John Doe', 43);
    """,
    """
    INSERT INTO Department VALUES('Interactive Media', 'Robert Brown', 82);
    """,
    """
    INSERT INTO Department VALUES('Biology', 'Mary Williams', 101);
    """
]

majorTuples = [
    """
    INSERT INTO Major VALUES('CSC', 'Computer Science', 'Computer Science');
    """,
    """
    INSERT INTO Major VALUES('CMK', 'Corporate Marketing', 'Marketing');
    """,
    """
    INSERT INTO Major VALUES('BIO', 'Biology', 'Biology');
    """,
    """
    INSERT INTO Major VALUES('MTH', 'Mathematics', 'Mathematics');
    """,
    """
    INSERT INTO Major VALUES('GDS', 'Game Design', 'Interactive Media');
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
    INSERT INTO Hosting VALUES('Interactive Media', 'Valentine Day Event');
    """,
    """
    INSERT INTO Hosting VALUES('Marketing', 'Homecoming');
    """,
    """
    INSERT INTO Hosting VALUES('Computer Science', 'Graduation');
    """,
    """
    INSERT INTO Hosting VALUES('Biology', 'Club Fair');
    """,
    """
    INSERT INTO Hosting VALUES('Computer Science', 'Club Fair');
    """,
    """
    INSERT INTO Hosting VALUES('Mathematics', 'Major Advising');
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
    """
]

allTuples = [departmentTuples, majorTuples, studentTuples, eventTuples, hostingTuples, decalringTuples, attendingTuples]

for relations in allTuples:
    print(relations)
    for tuples in relations:
        print(tuples)
        #cursor.execute(tuples)


# Insert row into table
# query = """
#    INSERT INTO Person
#    VALUES (1, "person1");
#    """
# cursor.execute(query)

# Select data
query = """
    SELECT s.stu_name, m.major_name
    FROM Student s, Major m
    """
cursor.execute(query)

# Extract column names from cursor
column_names = [row[0] for row in cursor.description]

# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)

# Examine dataframe
print(df)
print(df.columns)

# Example to extract a specific column
# print(df['name'])


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)


# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
