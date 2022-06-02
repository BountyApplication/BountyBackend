import sqlite3

# connecting to database
connection = sqlite3.connect('bounty.db')

# cursor
cursor = connection.cursor()

# SQL command to create a table in the database
sql_command = """CREATE TABLE accounts ( 
number INTEGER PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
balance FLOAT, 
joining DATE);"""
  
# execute the statement
cursor.execute(sql_command)

# close the connection
connection.close()